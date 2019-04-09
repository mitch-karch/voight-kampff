from lorem import discord_token, location_token, forecast_token, wolfram_token
from discord.ext.commands import Bot

from commands_library.weather_helper import weather_helper
from commands_library.dictionary_helper import urbanDict_helper
from commands_library.reddit_helper import reddit_top3
from commands_library.aug_helper import aug_init, aug_finder
from commands_library.wolfram_helper import wolf_short_query

BOT_PREFIX = (".")
client = Bot(command_prefix=BOT_PREFIX)
headers = {
    'cache-control': "no-cache",
}


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
    print(ctx.message.author.name +
          " requested for weather:" +
          request_location)
    em = weather_helper(request_location, location_token, forecast_token)
    await client.send_message(ctx.message.channel, embed=em)


@client.command(name="Urban Dictionary",
                description="Gives urban definitions",
                brief="Give ud",
                pass_context=True,
                aliases=['ud', 'urban'])
async def urbanDict(ctx, *, request_definition: str):
    print(ctx.message.author.name +
          " requested for definition:" +
          request_definition)
    em = urbanDict_helper(request_definition)
    await client.send_message(ctx.message.channel, embed=em)


@client.command(name="d_message",
                description="d_message",
                brief="d_message",
                pass_context=True,
                aliases=['d', 'D'])
async def d_message(ctx):
    print(ctx.message.author.name + " requested for d")
    await client.say("d")


@client.command(name="Reddit Top",
                description="Gives top three posts of reddit",
                brief="reddit",
                pass_context=True,
                aliases=['r', 'reddit'])
async def reddit_top(ctx, *, request_subreddit: str):
    print(ctx.message.author.name +
          " request_subreddited for reddit" +
          request_subreddit
          )
    em = reddit_top3(request_subreddit)
    await client.send_message(ctx.message.channel, embed=em)


@client.command(name="aug und",
                description="What's Aug Und Tier",
                brief="au",
                pass_context=True,
                aliases=['au', 'AU', 'aug', 'augund', 'autier'])
async def au_tier(ctx, *, word: str):
    print(ctx.message.author.name + " requested for au of " + word)
    constructedString = aug_finder(word)
    await client.say(constructedString)


@client.command(name="Wolfram Alpha",
                description="Query of the Wolfram|Alpha Short Answer API",
                brief="wa",
                pass_context=True,
                aliases=['wa', 'WA', 'wolf'])
async def wolfram(ctx, *, query: str):
    print(ctx.message.author.name + " requested for wolfram of " + query)
    em = wolf_short_query(query, wolfram_token)
    await client.send_message(ctx.message.channel, embed=em)


client.run(discord_token)
