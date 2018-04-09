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

    print("User requested for:" + request_loc)
    if(len(request_loc.split(" ")) > 1):
        request_loc = request_loc.replace(" ","%20")

    conn = http.client.HTTPConnection("autocomplete.wunderground.com")
    conn.request("GET", "/aq?query={loc}".format(loc=request_loc), headers=headers)
    res = conn.getresponse()
    data = res.read().decode("utf-8")
    json_response = json.loads(data)
    cityUrl = json_response["RESULTS"][0]["l"]
    cityName = json_response["RESULTS"][0]["name"]

    print("autoCompleted to:" + cityName)

    conn = http.client.HTTPConnection("api.wunderground.com")
    conn.request("GET", "/api/{apikey}/conditions/{location}.json".format(apikey=wunder_token,location=cityUrl), headers=headers)
    res = conn.getresponse()
    data = res.read()
    weather_response = json.loads(data)
    weather_f = weather_response["current_observation"]["temp_f"]
    
    await client.say("The weather in {city} is {temp} degrees F".format(city=cityName, temp=weather_f))

client.run(discord_token)
