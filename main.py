from lorem import discord_token, wunder_token, location_token, forecast_token
from discord.ext.commands import Bot
import discord
import http.client
import json
import random
import requests
import time

BOT_PREFIX = ("!",".")
client = Bot(command_prefix=BOT_PREFIX)
headers = {
    'cache-control': "no-cache",
}

augLibrary = {"sakai":True}

with open('dict.json', 'r') as f:
    augLibrary = json.load(f)

@client.event
async def on_ready():
    print("Logged in as " + client.user.name)
    print("------")

@client.command(name="Weather",
                description="Tells the weather",
                brief="Give Weather",
                pass_context=True,
                aliases=['w','weather'])
async def weather(ctx, *, request_location : str):
    print(ctx.message.author.name + " requested for weather:" + request_location)

    geocode_url = 'https://us1.locationiq.com/v1/search.php'
    # Use geocoding to get lat/lon
    conn = http.client.HTTPSConnection("")
    dataPayload = {
        'key' : location_token,
        'q' : request_location,
        'format' : 'json'
    }
    json_response = requests.get(geocode_url, params=dataPayload).json()
    lat = json_response[0]["lat"]
    lon = json_response[0]["lon"]
    cityName = json_response[0]["display_name"]

    print("autoCompleted to:" + cityName)

    # Get the weather conditions for the day
    conn = http.client.HTTPSConnection("api.darksky.net")
    conn.request("GET", "/forecast/{apikey}/{latitude},{longitude}"
                            .format(apikey=forecast_token,
                                    latitude=lat,
                                    longitude=lon)
                            )
    res = conn.getresponse()
    data = res.read()
    weather_response = json.loads(data)

    weather_f = weather_response["currently"]["temperature"]
    humidity = weather_response["currently"]["humidity"]
    dewpoint = weather_response["currently"]["dewPoint"]

    # Gather forecast summary information for the next two days.

    forecasts = []
    for i in range(3):
        inspectionTime = int(time.time()) + 60*60*24*i
        conn = http.client.HTTPSConnection("api.darksky.net")
        conn.request("GET", "/forecast/{apikey}/{latitude},{longitude},{timestamp}"
                                .format(apikey=forecast_token,
                                        latitude=lat,
                                        longitude=lon,
                                        timestamp=inspectionTime)
                                )
        res = conn.getresponse()
        data = res.read()
        weather_response = json.loads(data)
        print(weather_response["daily"]["data"][0]["summary"])
        forecasts.append(weather_response["daily"]["data"][0]["summary"])


    constructedString = ("The weather in **{city}** is **{temp}°F** with **{hum}** humidity. The dewpoint is **{dew}**°F\n"
                         "\n"
                         "Today's forecast: {tf}\n"
                         "Tomorrow: {f1}\n"
                         "The day after: {f2}\n")

    # Output all of it
    await client.say(constructedString.format(
                        city=cityName, 
                        temp=weather_f,
                        dew=dewpoint,
                        hum=humidity,
                        f1=forecasts[0],
                        f2=forecasts[1],
                        tf=forecasts[2])
                    )

@client.command(name="Urban Dictionary",
                description="Gives urban definitions",
                brief="Give ud",
                pass_context=True,
                aliases=['ud','urban'])
async def urbanDict(ctx, *, request_definition : str):

    print(ctx.message.author.name + " requested for definition:" + request_definition)
    char_lim=1000
    if(len(request_definition.split(" ")) > 1):
        request_definition = request_definition.replace(" ","%20")

    # Try to figure out where the user wanted to get info from
    conn = http.client.HTTPSConnection("api.urbandictionary.com")
    conn.request("GET", "/v0/define?term={stk}".format(stk=request_definition), headers=headers)
    json_response = json.loads(conn.getresponse().read().decode("utf-8"))
    definitions = json_response["list"]
    print(definitions[0]["definition"]);

    print("Urban Dictionary is:" + definitions[0]["word"])
    constructedString = ("__Urban Dictionary: ***{full}***__\n"
                        "\n"
                        "{defn}\n"
                        "*{example}*"
                        )
    await client.say(constructedString.format(
                        defn=(definitions[0]["definition"][:char_lim] + "__[truncated]__") if len(definitions[0]["definition"]) > char_lim else definitions[0]["definition"], 
                        full=definitions[0]["word"], 
                        example=(definitions[0]["example"][:char_lim] + "__[truncated]__") if len(definitions[0]["example"]) > char_lim else definitions[0]["example"], 
                        )
                    )
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
    conn = http.client.HTTPSConnection("www.reddit.com")
    conn.request("GET", "/r/{stk}/top/.json?limit=3".format(stk=request_subreddit), headers=headers)
    json_response = json.loads(conn.getresponse().read().decode("utf-8"))
    
    tops = json_response["data"]["children"]
    constructedString = ("__Top 3 posts: ***r/{full}***__\n"
                        "\n"
                        "1.{t0} <{t0u}>\n"
                        "2.{t1} <{t1u}>\n"
                        "3.{t2} <{t2u}>\n"
                        )
    em = discord.Embed(title="Top posts",
                        description= \
                            "1. ["+tops[0]['data']['title']+"]("+tops[0]['data']['url']+") | [comments](https://www.reddit.com"+tops[0]['data']['permalink']+")\n" + \
                            "2. ["+tops[1]['data']['title']+"]("+tops[1]['data']['url']+") | [comments](https://www.reddit.com"+tops[0]['data']['permalink']+")\n" + \
                            "3. ["+tops[2]['data']['title']+"]("+tops[2]['data']['url']+") | [comments](https://www.reddit.com"+tops[0]['data']['permalink']+")\n",
                        colour=0x0000FF)
    await client.send_message(ctx.message.channel, embed=em)
    """
    em.set_author(name="Top 3 subreddit posts: r/", url="www.reddit.com/r/",icon_url="https://cdn.discordapp.com/embed/avatars/0.png") 
    em.set_author(name="Top 3 subreddit posts: r/"+tops[0]["data"]["subreddit"], url="www.reddit.com/r/"+tops[0]["data"]["subreddit"],icon_url=client.user.default_avatar_url) 
    await client.say(constructedString.format(
                        full=tops[0]["data"]["subreddit"], 
                        t0=tops[0]["data"]["title"],
                        t1=tops[1]["data"]["title"],
                        t2=tops[2]["data"]["title"],
                        t0u=tops[0]["data"]["url"],
                        t1u=tops[1]["data"]["url"],
                        t2u=tops[2]["data"]["url"]
                        )
                    )
    """

@client.command(name="aug und",
                description="What's Aug Und Tier",
                brief="au",
                pass_context=True,
                aliases=['au','AU','aug', 'augund','autier'])
async def au_tier(ctx, *, word : str):
    print(ctx.message.author.name + " requested for au of" + word)
    #Check for existing value in dict
    auWord=False;
    if word in augLibrary:
        auWord = augLibrary[word]
    else:
        auWord = random.choice([True,False])
        augLibrary[word] = auWord
    with open('dict.json', 'w') as f:
        f.write(json.dumps(augLibrary))
    coinF = "is" if auWord else "is not"
    constructedString = "**{w}** __{c}__ aug und tier"
    await client.say(constructedString.format(c=coinF,w=word))

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
