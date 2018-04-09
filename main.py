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

    print(ctx.message.author.name + " requested for:" + request_loc)
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
    
    # Get some "nice text" for forecast
    conn = http.client.HTTPConnection("api.wunderground.com")
    conn.request("GET", "/api/{apikey}/forecast/{location}.json"
            .format(apikey=wunder_token,
                    location=cityUrl), 
                    headers=headers)
    res = conn.getresponse()
    data = res.read()
    weather_response = json.loads(data)
    forecast = weather_response["forecast"]["txt_forecast"]["forecastday"][0]["fcttext"]
    fore1 = weather_response["forecast"]["txt_forecast"]["forecastday"][1]["fcttext"]
    fore2 = weather_response["forecast"]["txt_forecast"]["forecastday"][2]["fcttext"]

    # Output all of it
    await client.say("The weather in **{city}** is **{temp}°F**, feels like **{feel_f}°F** with **{hum}** humidity.\n Today's forecast: {tf}. Tomorrow:{f1} \n The day after: {f2} ."
            .format(city=cityName, 
                    temp=weather_f,
                    feel_f=feels_f,
                    f1=fore1,
                    f2=fore2,
                    hum=humidity,
                    tf=forecast))

client.run(discord_token)
