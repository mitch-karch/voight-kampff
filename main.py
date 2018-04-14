from lorem import discord_token, wunder_token
from discord.ext.commands import Bot
import http.client
import json

BOT_PREFIX = ("!",".")
client = Bot(command_prefix=BOT_PREFIX)

@client.event
async def on_ready():
    print("Logged in as " + client.user.name)
    print("------")

@client.command(name="Weather",
                description="Tells the weather",
                brief="Give Weather",
                pass_context=True,
                aliases=['w','weather'])
async def weather(ctx, *, request_loc : str):
    headers = {
        'cache-control': "no-cache",
        }

    print(ctx.message.author.name + " requested for weather:" + request_loc)
    if(len(request_loc.split(" ")) > 1):
        request_loc = request_loc.replace(" ","%20")

    # Try to figure out where the user wanted to get info from
    conn = http.client.HTTPConnection("autocomplete.wunderground.com")
    conn.request("GET", "/aq?query={loc}".format(loc=request_loc), headers=headers)
    res = conn.getresponse()
    data = res.read().decode("utf-8")
    json_response = json.loads(data)
    cityUrl = json_response["RESULTS"][0]["l"]
    cityName = json_response["RESULTS"][0]["name"]

    print("autoCompleted to:" + cityName)

    # Get the weather conditions for the day
    conn = http.client.HTTPConnection("api.wunderground.com")
    conn.request("GET", "/api/{apikey}/conditions/{location}.json"
            .format(apikey=wunder_token,
                    location=cityUrl),
                    headers=headers)
    res = conn.getresponse()
    data = res.read()
    weather_response = json.loads(data)
    weather_f = weather_response["current_observation"]["temp_f"]
    feels_f = weather_response["current_observation"]["feelslike_f"]
    humidity = weather_response["current_observation"]["relative_humidity"]
    dewpoint = weather_response["current_observation"]["dewpoint_f"]
    
    # Get some "nice text" for forecast
    conn = http.client.HTTPConnection("api.wunderground.com")
    conn.request("GET", "/api/{apikey}/forecast/{location}.json"
            .format(apikey=wunder_token,
                    location=cityUrl), 
                    headers=headers)
    res = conn.getresponse()
    data = res.read()
    weather_response = json.loads(data)
    fore0 = weather_response["forecast"]["txt_forecast"]["forecastday"][0]["fcttext"]
    fore1 = weather_response["forecast"]["txt_forecast"]["forecastday"][1]["fcttext"]
    fore2 = weather_response["forecast"]["txt_forecast"]["forecastday"][2]["fcttext"]
    constructedString = ("The weather in **{city}** is **{temp}°F**, feels like **{feel_f}°F** with **{hum}** humidity. The dewpoint is **{dew}**°F\n"
                        "\n"
                        "Today's forecast:{tf}.\n"
                        "Tomorrow:{f1}\n"
                        "The day after:{f2}\n")

    # Output all of it
    await client.say(constructedString.format(
                        city=cityName, 
                        temp=weather_f,
                        feel_f=feels_f,
                        f1=fore1,
                        f2=fore2,
                        dew=dewpoint,
                        hum=humidity,
                        tf=fore0)
                    )

@client.command(name="Urban Dictionary",
                description="Gives urban definitions",
                brief="Give ud",
                pass_context=True,
                aliases=['ud','urban'])
async def stocks(ctx, *, request_def : str):
    headers = {
        'cache-control': "no-cache",
        }

    print(ctx.message.author.name + " requested for definition:" + request_def)
    if(len(request_def.split(" ")) > 1):
        request_def = request_def.replace(" ","%20")

    # Try to figure out where the user wanted to get info from
    conn = http.client.HTTPSConnection("api.urbandictionary.com")
    conn.request("GET", "/v0/define?term={stk}".format(stk=request_def), headers=headers)
    res = conn.getresponse()
    data = res.read().decode("utf-8")
    json_response = json.loads(data)
    definitions = json_response["list"]

    print("Urban Dictionary is:" + definitions[0]["word"])
    constructedString = ("__Urban Dictionary: ***{full}***__\n"
                        "\n"
                        "{defn}\n"
                        "*{example}*"
                        )
    await client.say(constructedString.format(
                        defn=definitions[0]["definition"], 
                        full=definitions[0]["word"], 
                        example=definitions[0]["example"]
                        )
                    )
@client.command(name="d_message",
                description="d_message",
                brief="d_message",
                pass_context=True,
                aliases=['d','dd'])
async def d_message(ctx):
    print(ctx.message.author.name + " requested for d")
    await client.say("d")

client.run(discord_token)
