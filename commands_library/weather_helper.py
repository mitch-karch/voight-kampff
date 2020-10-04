from discord import Embed
from commands_library.query_helper import payload_request, query_request
from helper_functions.logger import general_debug, general_info
from helper_functions.urlBuilder import urlBuilder
from helper_functions.errorHelpers import errorEmbedBuilder

import datetime
import time
import json

geocode_url = "https://us1.locationiq.com/v1/search.php"

emojiDict = {
    "01d": "☀️",
    "01n": "🌙",
    "02d": "⛅",
    "02n": "☁️",
    "03d": "☁️",
    "03n": "☁️",
    "04d": "☁️",
    "04n": "☁️",
    "09d": "🌧️",
    "09n": "🌧️",
    "10d": "🌧️",
    "10n": "🌧️",
    "11d": "🌩️",
    "11n": "🌩️",
    "13d": "🌨️",
    "13n": "🌨️",
    "50d": "🌫️",
    "50n": "🌫️",
}
user_library = {}


def user_init():
    global user_library
    with open("user_weather.json", "r") as f:
        user_library = json.load(f)


def weather_helper_repeat_user(request_user, location_token, forecast_token):
    try:
        if str(request_user) in user_library:
            lon = user_library[request_user]["lon"]
            lat = user_library[request_user]["lat"]
            return weather_helper(
                request_user, "congo", location_token, forecast_token, lat, lon
            )
    except KeyError:
        return errorEmbedBuilder("Sorry, I have no memory of your user", "Weather")


def weather_helper(
    user_name, request_location: str, location_token, forecast_token, lat=None, lon=None
):
    if lat is None and lon is None:
        # Use geocoding to get lat/lon
        dataPayload = {"key": location_token, "q": request_location, "format": "json"}
        geo_response = payload_request(geocode_url, dataPayload)

        general_debug(
            "Location is: " + geo_response[0]["lat"] + "," + geo_response[0]["lon"]
        )

        lon = geo_response[0]["lon"]
        lat = geo_response[0]["lat"]
        city_name = geo_response[0]["display_name"]
        user_library[str(user_name)] = {"lat": lat, "lon": lon, "city_name": city_name}
        with open("user_weather.json", "w") as f:
            f.write(json.dumps(user_library))

    # Get the weather conditions for the day
    wea_response = query_request(
        "api.openweathermap.org",
        "/data/2.5/onecall?lat={latitude}&lon={longitude}&appid={apikey}&units=imperial".format(
            apikey=forecast_token, latitude=lat, longitude=lon
        ),
    )

    general_info("Weather is: " + str(wea_response))

    weather_f = wea_response["current"]["temp"]
    humidity = str(wea_response["current"]["humidity"]) + "%"
    dewpoint = wea_response["current"]["dew_point"]
    summary = wea_response["current"]["weather"][0]["description"].title()

    # Gather forecast summary information for the next two days.

    mainString = (
        "It is currently **{temp}°F** "
        "with **{hum}** humidity "
        "and a dewpoint of **{dew}**°F\n"
        "A description of the weather: {sum}"
    ).format(temp=weather_f, dew=dewpoint, hum=humidity, sum=summary)
    # Output all of it
    em = Embed(
        title="Weather in " + user_library[user_name]["city_name"],
        description=mainString,
        colour=0x00FF00,
    )

    days = ["Today", "Tomorrow", "Day After"]
    for i, day in enumerate(days):
        em.add_field(
            name=day
            + "'s forecast "
            + "("
            + str(wea_response["daily"][i]["temp"]["max"])
            + "/"
            + str(wea_response["daily"][i]["temp"]["min"])
            + "):",
            value=emojiDict[wea_response["daily"][i]["weather"][0]["icon"]]
            + " "
            + wea_response["daily"][i]["weather"][0]["description"].title(),
        )

    general_info("Weather created and returned embed object")
    return em
