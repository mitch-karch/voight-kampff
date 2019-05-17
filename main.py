from lorem import discord_token, location_token, forecast_token, wolfram_token, imgur_id, webster_definition_token # noqa: 501

from helper_functions.logger import command_log_info

from discord.ext.commands import Bot

from commands_library.weather_helper import weather_helper
from commands_library.dictionary_helper import urbanDict_helper, urbanDict_multiple # noqa: 501
from commands_library.reddit_helper import reddit_top3
from commands_library.aug_helper import aug_init, aug_finder
from commands_library.wolfram_helper import wolf_short_query
from commands_library.imgur_helper import imgur_top
from commands_library.webster_helper import websterDict_helper


BOT_PREFIX = (".")
client = Bot(command_prefix=BOT_PREFIX)


@client.event
async def on_ready():
    print("Logged in as " + client.user.name)
    print("------")
    aug_init()


@client.event
async def on_message(message):
    if 'thank you baptiste' in message.content:
        print("Oh! You're welcome")
        await client.send_message(message.channel, "Oh! You're welcome")
        # Do stuff here
    await client.process_commands(message)


@client.command(name="Weather",
                description="Tells the weather",
                brief="Give Weather",
                pass_context=True,
                aliases=['w', 'weather'])
async def weather(ctx, *, request_location: str):
    command_log_info(ctx.message.author.name, "weather", request_location)
    em = weather_helper(request_location, location_token, forecast_token)
    await client.send_message(ctx.message.channel, embed=em)


@client.command(name="Urban Dictionary",
                description="Gives urban definitions",
                brief="Give ud",
                pass_context=True,
                aliases=['ud', 'urban', 'UD'])
async def urbanDict(ctx, *args):
    if len(args) == 2 and args[1].isdigit():
        request_definition = args[0]
        numOfDefs = int(args[1])
        command_log_info(ctx.message.author.name,
                         "multiple urbanDict",
                         request_definition + str(numOfDefs)
                         )
        em = urbanDict_multiple(request_definition, numOfDefs)
    else:
        request_definition = " ".join(args)
        command_log_info(ctx.message.author.name,
                         "single urbanDict",
                         request_definition
                         )
        em = urbanDict_helper(request_definition)

    await client.send_message(ctx.message.channel, embed=em)


@client.command(name="d_message",
                description="d_message",
                brief="d_message",
                pass_context=True,
                aliases=['d', 'D'])
async def d_message(ctx):
    command_log_info(ctx.message.author.name, "d", "d")
    await client.say("d")


@client.command(name="Reddit Top",
                description="Gives top three posts of reddit",
                brief="reddit",
                pass_context=True,
                aliases=['r', 'reddit'])
async def reddit_top(ctx, *, request_subreddit: str):
    command_log_info(ctx.message.author.name, "reddit", request_subreddit)
    em = reddit_top3(request_subreddit)
    await client.send_message(ctx.message.channel, embed=em)


@client.command(name="aug und",
                description="What's Aug Und Tier",
                brief="au",
                pass_context=True,
                aliases=['au', 'AU', 'aug', 'augund', 'autier'])
async def au_tier(ctx, *, request_word: str):
    command_log_info(ctx.message.author.name, "au_tier", request_word)
    constructedString = aug_finder(request_word)
    await client.say(constructedString)


@client.command(name="Wolfram Alpha",
                description="Query of the Wolfram|Alpha Short Answer API",
                brief="wa",
                pass_context=True,
                aliases=['wa', 'WA', 'wolf'])
async def wolfram(ctx, *, request_query: str):
    command_log_info(ctx.message.author.name, "wolfram", request_query)
    em = wolf_short_query(request_query, wolfram_token)
    await client.send_message(ctx.message.channel, embed=em)


@client.command(name="Imgur Top Images",
                description="Query top image result from Imgur API",
                brief="im",
                pass_context=True,
                aliases=['im', 'IM', 'imgur', 'img'])
async def imgur(ctx, *, request_query: str):
    command_log_info(ctx.message.author.name, "imgur", request_query)
    em = imgur_top(request_query, imgur_id)
    await client.send_message(ctx.message.channel, embed=em)

webster_definition_token 

@client.command(name="Webster Dictionary",
                description="Gives Webster definitions",
                brief="Give def",
                pass_context=True,
                aliases=['dd', 'webster', 'DD'])
async def websterLookup(ctx, *, request_definition: str):
    command_log_info(ctx.message.author.name,
                     "Webster Definition",
                     request_definition
                     )
    em = websterDict_helper(request_definition, webster_definition_token)

    await client.send_message(ctx.message.channel, embed=em)

client.run(discord_token)
