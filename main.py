#!bin/python3

from lorem import *

from helper_functions.logger import command_log_info

from discord import TextChannel
from discord.ext import tasks, commands
from discord.ext.commands import Bot

from discord.embeds import Embed

from commands_library.weather_helper import (
    weather_helper,
    weather_helper_repeat_user,
    user_init,
)
from commands_library.dictionary_helper import (
    urbanDict_helper,
    urbanDict_multiple,
)  # noqa: 501
from commands_library.reddit_helper import reddit_top3
from commands_library.aug_helper import aug_init, aug_finder
from commands_library.wolfram_helper import wolf_short_query
from commands_library.imgur_helper import imgur_top
from commands_library.webster_helper import websterDict_helper
from commands_library.wiki_helper import wiki_helper
from commands_library.roll_helper import roll_helper
from commands_library.random_helper import random_helper
from commands_library.spotify_helper import SpotifyBot
from commands_library.reminders_helper import Clock
from commands_library.reminders_helper import Reminders
from commands_library.time_helper import time_helper
from commands_library.typing_helper import typing_detector
from helper_functions.text_checker import dictionary_lookup, response_init

import logging

BOT_PREFIX = "."
client = Bot(command_prefix=BOT_PREFIX)


async def send_reminder(kind, channel, who, message):
    logging.info(
        "send kind = %s channel = %s who = %s message = %s", kind, channel, who, message
    )
    if kind == "reminder":
        user = client.get_user(who["id"])
        await user.send(message)
    if kind == "timer":
        ch = client.get_channel(channel["id"])
        await ch.send("Ding ding ding: " + message)


spotifyBot = SpotifyBot()
reminders = Reminders("reminders.json", send_reminder)
reminders.load()
clock = Clock(reminders)


@tasks.loop(seconds=1.0)
async def clock_tick():
    await clock.tick()


@client.event
async def on_ready():
    print("Logged in as " + client.user.name)
    print("------")
    reminders.load()
    clock_tick.start()
    aug_init()
    user_init()
    response_init()


@client.event
async def on_message(message):
    tempLookup = dictionary_lookup(message.content)
    if tempLookup is not False:
        await message.channel.send(tempLookup)

    if isinstance(message.channel, TextChannel):
        spotifyBot.on_message(message.channel.name, message.content)

    await client.process_commands(message)


@client.event
async def on_typing(channel, user, when):
    yell_message = typing_detector(channel.id, user.id, when)
    if yell_message is not None:
        await channel.send(yell_message)


@client.command(
    name="Weather",
    description="Gives the three day forecast for a request location. Weather sourced from DarkSky",  # noqa: 501
    brief="Gives weather for a location",
    pass_context=True,
    aliases=["w", "weather"],
)
async def weather(ctx, *, request_location=None):
    command_log_info(ctx.message.author.name, "weather", str(request_location))
    if request_location is None:
        em = weather_helper_repeat_user(
            str(ctx.message.author.id), location_token, forecast_token
        )
    else:
        em = weather_helper(
            str(ctx.message.author.id), request_location, location_token, forecast_token
        )
    await ctx.message.channel.send(embed=em)


@client.command(
    name="Reminders",
    description="Use the reminder_spec of <length><time> <message> such as '1hour do thing'",
    brief="Remidners",
    pass_context=True,
    aliases=["remind"],
)
async def reminder(ctx, *, reminder_spec: str):
    command_log_info(ctx.message.author.name, "reminder", reminder_spec)
    channel = {
        "id": ctx.message.channel.id,
        "name": str(ctx.message.channel),
    }
    author = {
        "id": ctx.message.author.id,
        "name": ctx.message.author.name,
    }
    em = clock.on_reminder(channel, author, reminder_spec)
    if em:
        await ctx.message.channel.send(embed=em)


@client.command(
    name="Timers",
    description="Timers",
    brief="Timers",
    pass_context=True,
    aliases=["timer"],
)
async def timer(ctx, *, timer_spec: str):
    command_log_info(ctx.message.author.name, "timer", timer_spec)
    channel = {
        "id": ctx.message.channel.id,
        "name": str(ctx.message.channel),
    }
    author = {
        "id": ctx.message.author.id,
        "name": ctx.message.author.name,
    }
    em = clock.on_timer(channel, author, timer_spec)
    if em:
        await ctx.message.channel.send(embed=em)


@client.command(
    name="Time", description="Time", brief="Time", pass_context=True, aliases=["time"],
)
async def time(ctx, *, query: str):
    command_log_info(ctx.message.author.name, "time", query)
    em = time_helper(query)
    if em:
        await ctx.message.channel.send(embed=em)


@client.command(
    name="Urban Dictionary",
    description="Gives urban definitions for words. Can pass an integer(N) after the definition to return the top N definitions",  # noqa: 501
    brief="Gives Urban Dictionary definitions",
    pass_context=True,
    aliases=["ud", "urban", "UD"],
)
async def urbanDict(ctx, *args):
    if len(args) == 2 and args[1].isdigit():
        request_definition = args[0]
        numOfDefs = int(args[1])
        command_log_info(
            ctx.message.author.name,
            "multiple urbanDict",
            request_definition + str(numOfDefs),
        )
        em = urbanDict_multiple(request_definition, numOfDefs)
    else:
        request_definition = " ".join(args)
        command_log_info(
            ctx.message.author.name, "single urbanDict", request_definition
        )
        em = urbanDict_helper(request_definition)

    await ctx.message.channel.send(embed=em)


@client.command(
    name="d_message",
    description="Shorthand ping message",
    brief="Shorthand ping message",
    pass_context=True,
    aliases=["d", "D"],
)
async def d_message(ctx):
    command_log_info(ctx.message.author.name, "d", "d")
    await ctx.message.channel.send("d")


@client.command(
    name="Reddit Top",
    description="Gives top three posts of specific subreddit. If subreddit has less than 3 recent posts, an error will be returned.",  # noqa: 501
    brief="Gives top 3 posts of given subreddit",
    pass_context=True,
    aliases=["r", "reddit"],
)
async def reddit_top(ctx, *, request_subreddit: str):
    command_log_info(ctx.message.author.name, "reddit", request_subreddit)
    em = reddit_top3(request_subreddit)
    await ctx.message.channel.send(embed=em)


@client.command(
    name="aug und",
    description="Returns if a subject is Aug Und Tier",
    brief="Returns if a subject is Aug Und Tier",
    pass_context=True,
    aliases=["au", "AU", "aug", "augund", "autier"],
)
async def au_tier(ctx, *, request_word: str):
    command_log_info(ctx.message.author.name, "au_tier", request_word)
    constructedString = aug_finder(request_word)
    await ctx.message.channel.send(constructedString)


@client.command(
    name="Wolfram Alpha",
    description="Query of the Wolfram|Alpha Short Answer API",
    brief="Returns a short answer of a given wolfram query",
    pass_context=True,
    aliases=["wa", "WA", "wolf"],
)
async def wolfram(ctx, *, request_query: str):
    command_log_info(ctx.message.author.name, "wolfram", request_query)
    em = wolf_short_query(request_query, wolfram_token)
    await ctx.message.channel.send(embed=em)


@client.command(
    name="Imgur Top Images",
    description="Query top image result from Imgur API",
    brief="Returns top viral image result from Imgur",
    pass_context=True,
    aliases=["im", "IM", "imgur", "img"],
)
async def imgur(ctx, *, request_query: str):
    command_log_info(ctx.message.author.name, "imgur", request_query)
    em = imgur_top(request_query, imgur_id)

    # Note: This is not good form but is a quick way to get the intended
    # behavior. Currently discord embeds do not support anything other than
    # image filetypes. Imgur likes to use .mp4 which do not like to be used in
    # embed data types. So if it's a video/mp4 type we just return the string
    # and paste it directly to the channel where discord will embed it by
    # itself. Technically this loses the link to the album which ruins the
    # purpose of embed systems, but its a sacrifice and should be looked into
    # soon.

    if isinstance(em, Embed):
        await ctx.message.channel.send(embed=em)
    elif isinstance(em, str):
        await ctx.message.channel.send(em)


@client.command(
    name="Wikipedia",
    description="Looks up wikipedia entries based on query",
    brief="Looks up wikipedia",
    pass_context=True,
    aliases=["wi", "wiki"],
)
async def websterLookup(ctx, *, request_definition: str):
    command_log_info(ctx.message.author.name, "Webster Definition", request_definition)
    em = wiki_helper(request_definition)

    await ctx.message.channel.send(embed=em)


@client.command(
    name="Webster Dictionary",
    description="Gives Webster definitions",
    brief="Gives english definition",
    pass_context=True,
    aliases=["dd", "webster", "DD"],
)
async def websterLookup(ctx, *, request_definition: str):
    command_log_info(ctx.message.author.name, "Webster Definition", request_definition)
    em = websterDict_helper(request_definition, webster_definition_token)

    await ctx.message.channel.send(embed=em)


@client.command(
    name="Dice Roll",
    description="Return a variety of random values",
    brief="Return a random value",
    pass_context=True,
    aliases=["roll", "dice"],
)
async def roll(ctx, *, dice_spec: str = "d2"):
    command_log_info(ctx.message.author.name, "diceRoll", str(dice_spec))
    await ctx.message.channel.send(embed=roll_helper(dice_spec))


@client.command(
    name="UUID",
    description="Return a hex value of UUID",
    brief="Return a random UUID",
    pass_context=True,
    aliases=["uuid"],
)
async def uuidGenerator(ctx, *, request_value=0):
    command_log_info(ctx.message.author.name, "uuid", str(request_value))
    em = random_helper("UUID", request_value)
    await ctx.message.channel.send(embed=em)


if __name__ == "__main__":
    spotifyBot.initialize()
    client.run(discord_token)
