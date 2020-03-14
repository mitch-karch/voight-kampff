from datetime import datetime, timedelta

import logging
import sys

recentMessages = {}

lastShout = datetime.utcnow()
refractory_period = timedelta(seconds=10)
timeLimit = 3
userLimit = 5
timeAdjust = timedelta(seconds=timeLimit)


def get_active_typers(now):
    return [
        x
        for x in recentMessages[channel.id].values()
        if x > now - timeAdjust and x <= now
    ]


def typing_detector(channel, user, when, now=None):
    if not now:
        now = when

    global lastShout

    user = user.id

    if channel.id not in recentMessages:
        recentMessages[channel.id] = {}

    recentMessages[channel.id][user] = when

    typers = get_active_typers(now)

    print(recentMessages, len(typers))

    if len(typers) > userLimit:
        if lastShout + timedelta(seconds=60) < datetime.utcnow():
            lastShout = now
            print("several")
            return "SEVERAL PEOPLE ARE TYPING"
        else:
            print("several, throttled")


# Or namedtuple
class FakeChannel:
    def __init__(self, id):
        self.id = id


# Or namedtuple
class FakeUser:
    def __init__(self, id):
        self.id = id


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    channel = FakeChannel("test")

    clock = datetime.utcnow()

    lastShout = clock - timedelta(seconds=300)

    assert (
        typing_detector(channel, FakeUser("jacob"), clock + timedelta(seconds=0.1))
        == None
    )
    assert (
        typing_detector(channel, FakeUser("carla"), clock + timedelta(seconds=1))
        == None
    )
    assert (
        typing_detector(channel, FakeUser("bob"), clock + timedelta(seconds=1)) == None
    )
    assert (
        typing_detector(channel, FakeUser("bill"), clock + timedelta(seconds=1.5))
        == None
    )
    assert (
        typing_detector(channel, FakeUser("joe"), clock + timedelta(seconds=2)) == None
    )
    assert (
        typing_detector(channel, FakeUser("john"), clock + timedelta(seconds=2))
        == "SEVERAL PEOPLE ARE TYPING"
    )
    assert (
        typing_detector(channel, FakeUser("john"), clock + timedelta(seconds=2)) == None
    )

    # ignore future types
    assert len(get_active_typers(clock)) == 0

    # typers up until john
    assert len(get_active_typers(clock + timedelta(seconds=2))) == 6

    # cause jacob to drop
    assert len(get_active_typers(clock + timedelta(seconds=0.1 + timeLimit))) == 5
