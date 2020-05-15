from discord import Embed
from commands_library.query_helper import payload_request, query_request
from helper_functions.logger import general_debug, general_info
from helper_functions.urlBuilder import urlBuilder
from helper_functions.errorHelpers import errorEmbedBuilder

import datetime
import time
import json

weather_baseUrl = "https://darksky.net/forecast/"
details_baseUrl = "https://darksky.net/details/"
emojiDict = {
    "clear-day": "☀️",
    "clear-night": "🌙",
    "rain": "🌧️",
    "snow": "🌨️",
    "sleet": "☃️",
    "wind": "🍃",
    "fog": "🌫️",
    "cloudy": "☁️",
    "partly-cloudy-day": "⛅",
    "partly-cloudy-night": "☁️",
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
        geocode_url = "https://us1.locationiq.com/v1/search.php"
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
        "api.darksky.net",
        "/forecast/{apikey}/{latitude},{longitude}".format(
            apikey=forecast_token, latitude=lat, longitude=lon
        ),
    )

    general_debug("Weather is: " + str(wea_response))

    weather_f = wea_response["currently"]["temperature"]
    humidity = "{:.1%}".format(wea_response["currently"]["humidity"])
    dewpoint = wea_response["currently"]["dewPoint"]

    # Gather forecast summary information for the next two days.

    forecasts = []
    for i in range(3):
        inspectionTime = int(time.time()) + 60 * 60 * 24 * i
        wea_response = query_request(
            "api.darksky.net",
            "/forecast/{key}/{latit},{longi},{tim}".format(
                key=forecast_token, latit=lat, longi=lon, tim=inspectionTime
            ),
        )
        tempObj = wea_response
        forecasts.append(tempObj)

    # mainUrl = weather_baseUrl + str(lat) + ',' + str(lon)
    detailsUrl = details_baseUrl + str(lat) + "," + str(lon)

    mainString = (
        "It is currently **{temp}°F** "
        "with **{hum}** humidity "
        "and a dewpoint of **{dew}**°F\n"
    ).format(temp=weather_f, dew=dewpoint, hum=humidity,)
    # Output all of it
    em = Embed(
        title="Weather in " + user_library[user_name]["city_name"],
        description=mainString,
        colour=0x00FF00,
    )

    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    dayAfter = today + datetime.timedelta(days=2)
    em.add_field(
        name="Today's forecast "
        + "("
        + str(forecasts[0]["daily"]["data"][0]["temperatureHigh"])
        + "/"
        + str(forecasts[0]["daily"]["data"][0]["temperatureLow"])
        + "):",
        value=emojiDict[forecasts[0]["daily"]["data"][0]["icon"]]
        + urlBuilder(
            forecasts[0]["daily"]["data"][0]["summary"], detailsUrl + "/" + str(today)
        ),
    )

    em.add_field(
        name="Tomorrow's forecast "
        + "("
        + str(forecasts[1]["daily"]["data"][0]["temperatureHigh"])
        + "/"
        + str(forecasts[1]["daily"]["data"][0]["temperatureLow"])
        + "):",
        value=emojiDict[forecasts[1]["daily"]["data"][0]["icon"]]
        + urlBuilder(
            forecasts[1]["daily"]["data"][0]["summary"],
            detailsUrl + "/" + str(tomorrow),
        ),
    )

    em.add_field(
        name="Day After's forecast "
        + "("
        + str(forecasts[2]["daily"]["data"][0]["temperatureHigh"])
        + "/"
        + str(forecasts[2]["daily"]["data"][0]["temperatureLow"])
        + "):",
        value=emojiDict[forecasts[2]["daily"]["data"][0]["icon"]]
        + urlBuilder(
            forecasts[2]["daily"]["data"][0]["summary"],
            detailsUrl + "/" + str(dayAfter),
        ),
    )

    general_info("Weather created and returned embed object")
    return em
