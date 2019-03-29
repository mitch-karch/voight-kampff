import http.client
import requests
import json
import time


def weather_helper(request_location: str, location_token, forecast_token):

    geocode_url = 'https://us1.locationiq.com/v1/search.php'
    # Use geocoding to get lat/lon
    conn = http.client.HTTPSConnection("")
    dataPayload = {
        'key': location_token,
        'q': request_location,
        'format': 'json'
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
        conn.request("GET", "/forecast/{key}/{latit},{longi},{timestamp}"
                            .format(key=forecast_token,
                                    latit=lat,
                                    longi=lon,
                                    timestamp=inspectionTime)
                     )
        res = conn.getresponse()
        data = res.read()
        weather_response = json.loads(data)
        print(weather_response["daily"]["data"][0]["summary"])
        forecasts.append(weather_response["daily"]["data"][0]["summary"])

    constructedString = ("The weather in **{city}** is **{temp}°F**"
                         "with **{hum}** humidity."
                         "The dewpoint is **{dew}**°F\n"
                         "\n"
                         "Today's forecast: {tf}\n"
                         "Tomorrow: {f1}\n"
                         "The day after: {f2}\n")

    # Output all of it
    return constructedString.format(
                        city=cityName,
                        temp=weather_f,
                        dew=dewpoint,
                        hum=humidity,
                        f1=forecasts[0],
                        f2=forecasts[1],
                        tf=forecasts[2])
