import logging
import json
import sys
import os
import time

import parsedatetime
import datetime
import pytz

import discord

HuhWhen = "huh, when?"
GotYou = "i got you"

class Reminders:
    def __init__(self, fn, send_message):
        self.log = logging.getLogger("reminders")
        self.fn = fn
        self.send_message = send_message
        self.cal = parsedatetime.Calendar()
        self.reminders = {
            "reminders": []
        }

    def load(self):
        if os.path.isfile(self.fn):
            with open(self.fn) as f:
                self.reminders = json.load(f)
        return self.reminders

    def save(self):
        with open(self.fn, "w") as f:
            json.dump(self.reminders, f)

    def remember(self, kind, channel, author, spec):
        try:
            self.log.info("#%s author = %s spec = '%s'", channel, author, spec)

            parts = spec.split(" ")
            when, status = self.cal.parse(parts[0]) #, datetime.datetime.now(pytz.timezone('UTC')))

            if False: self.log.info("status = %s when = %s", status, when)

            if status == 0:
                return HuhWhen

            now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            reply_time = time.strftime('%Y-%m-%d %H:%M:%S', when)
            diff = time.mktime(when) - time.time()

            self.log.info("time = %s (diff = %s)", reply_time, diff)

            self.reminders["reminders"].append({
                "kind": kind,
                "created": now_time,
                "channel": channel,
                "author": author,
                "message": spec,
                "alarm_pretty": reply_time,
                "alarm": time.mktime(when),
            })

            self.reminders["reminders"].sort(key=lambda x: x["alarm"])

            return GotYou
        except Exception as e:
            self.log.warn(e)
            return HuhWhen

    async def check(self):
        now = time.time()
        all = self.reminders["reminders"]
        while len(all) > 0:
            if all[0]["alarm"] > now:
                break

            self.log.info("%s > %s", all[0]["alarm"], now)
            reminder = all.pop(0)
            await self.remind(reminder)

        self.save()

    async def remind(self, reminder):
        self.log.info("remind %s", reminder)
        await self.send_message(reminder['kind'], reminder['channel'], reminder['author'], reminder['message'])

class Clock:
    def __init__(self, reminders):
        self.r = reminders
        self.log = logging.getLogger("clock")

    async def tick(self):
        await self.r.check()

    def on_reminder(self, channel, author, spec):
        self.r.load()
        message = self.r.remember('reminder', channel, author, spec)
        self.r.save()
        if message: return discord.Embed(title="Reminder", description=message, colour=0xFFFF00)
        return None

    def on_timer(self, channel, author, spec):
        self.r.load()
        message = self.r.remember('timer', channel, author, spec)
        self.r.save()
        if message: return discord.Embed(title="Timer", description=message, colour=0xFFFF00)
        return None

async def dev_null_message(kind, channel, who, message):
    logging.info("send who = %s message = %s", who, message)

if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    r = Reminders("reminders-test.json", dev_null_message)

    author = {
        "id": 1,
        "name": "jacob",
    }

    channel = {
        "id": 1,
        "name": "test",
    }

    r.load()
    assert r.remember('reminder', channel, author, "nothing") == HuhWhen
    assert r.remember('reminder', channel, author, "something else") == HuhWhen
    assert r.remember('reminder', channel, author, "1") == HuhWhen
    assert r.remember('reminder', channel, author, "5s") == HuhWhen
    assert r.remember('reminder', channel, author, "1hour hour") == GotYou
    assert r.remember('reminder', channel, author, "5seconds five seconds") == GotYou
    assert r.remember('reminder', channel, author, "1day 1 day") == GotYou
    r.save()

    c = Clock(r)
