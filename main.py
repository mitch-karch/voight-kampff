from lorem import discord_token, wunder_token, location_token, forecast_token
from discord.ext.commands import Bot
import discord
import http.client
import random
import time
import requests
import json

from commands_library.weather_helper import weather_helper
from commands_library.dictionary_helper import urbanDict_helper
from commands_library.reddit_helper import reddit_top3
from commands_library.aug_helper import aug_init, aug_finder
#import commands_library.query_helper

BOT_PREFIX = ("!",".")
client = Bot(command_prefix=BOT_PREFIX)
headers = {
    'cache-control': "no-cache",
}


@client.event
async def on_ready():
    print("Logged in as " + client.user.name)
    print("------")
    aug_init()

@client.command(name="Weather",
                description="Tells the weather",
                brief="Give Weather",
                pass_context=True,
                aliases=['w','weather'])
async def weather(ctx, *, request_location : str):
    print(ctx.message.author.name + " requested for weather:" + request_location)
    constructedString = weather_helper(request_location, location_token, forecast_token)
    await client.say(constructedString)

@client.command(name="Urban Dictionary",
                description="Gives urban definitions",
                brief="Give ud",
                pass_context=True,
                aliases=['ud','urban'])
async def urbanDict(ctx, *, request_definition : str):
    print(ctx.message.author.name + " requested for definition:" + request_definition)
    constructedString = urbanDict_helper(request_definition)
    await client.say(constructedString)

@client.command(name="d_message",
                description="d_message",
                brief="d_message",
                pass_context=True,
                aliases=['d','D'])
async def d_message(ctx):
    print(ctx.message.author.name + " requested for d")
    await client.say("d")

@client.command(name="Reddit Top",
                description="Gives top three posts of reddit",
                brief="reddit",
                pass_context=True,
                aliases=['r','reddit'])
async def reddit_top(ctx, *, request_subreddit: str ):
    print(ctx.message.author.name + " request_subreddited for reddit" + request_subreddit)
    em = reddit_top3(request_subreddit)
    await client.send_message(ctx.message.channel, embed=em)

@client.command(name="aug und",
                description="What's Aug Und Tier",
                brief="au",
                pass_context=True,
                aliases=['au','AU','aug', 'augund','autier'])
async def au_tier(ctx, *, word : str):
    print(ctx.message.author.name + " requested for au of " + word)
    constructedString = aug_finder(word)
    await client.say(constructedString)

@client.command(name="Stocks",
                description="Gives daily stock information",
                brief="Give stocks",
                pass_context=True,
                aliases=['$','price'])
async def stocks(ctx, *, request_stock : str):
    print(ctx.message.author.name + " requested for stock:" + request_stock)
    if(len(request_stock.split(" ")) > 1):
        request_stock = request_stock.replace(" ","%20")
    conn = http.client.HTTPSConnection("api.iextrading.com")
    conn.request("GET", "/1.0/stock/{stk}/batch?types=quote,news".format(stk=request_stock), headers=headers)

    json_response = json.loads(conn.getresponse().read().decode("utf-8"))

    latestPrice = json_response["quote"]["latestPrice"]
    symbol = json_response["quote"]["symbol"]
    companyName = json_response["quote"]["companyName"]
    companyQuote = json_response["quote"]
    companyNews = json_response["news"]

    print("Stock is:" + companyName)
    constructedString = ("**{full}** (Symbol: *{short}*): ${last} ({pChange}%) \n"
                        "\n"
                        "__News for {full}:__\n"
                        "\n"
                        "{n0}: <{n0u}>\n"
                        "{n1}: <{n1u}>\n"
                        "{n2}: <{n2u}>\n"
                        )
    await client.say(constructedString.format(
                        full=companyName, 
                        short=symbol, 
                        last=latestPrice,
                        n0=companyNews[0]["headline"],
                        n1=companyNews[1]["headline"],
                        n2=companyNews[2]["headline"],
                        n0u=companyNews[0]["url"],
                        n1u=companyNews[1]["url"],
                        n2u=companyNews[2]["url"],
                        pChange=companyQuote["changePercent"]
                        )
                    )
client.run(discord_token)
