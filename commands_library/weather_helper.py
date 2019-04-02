from commands_library.query_helper import payload_request, query_request
import time


def weather_helper(request_location: str, location_token, forecast_token):

    geocode_url = 'https://us1.locationiq.com/v1/search.php'
    # Use geocoding to get lat/lon
    dataPayload = {
        'key': location_token,
        'q': request_location,
        'format': 'json'
    }
    geo_response = payload_request(geocode_url, dataPayload)

    lon = geo_response[0]["lon"]
    lat = geo_response[0]["lat"]
    cityName = geo_response[0]["display_name"]

    print("autoCompleted to:" + cityName)

    # Get the weather conditions for the day
    wea_response = query_request("api.darksky.net",
                                 "/forecast/{apikey}/{latitude},{longitude}"
                                 .format(apikey=forecast_token,
                                         latitude=lat,
                                         longitude=lon
                                         )
                                 )

    weather_f = wea_response["currently"]["temperature"]
    humidity = wea_response["currently"]["humidity"]
    dewpoint = wea_response["currently"]["dewPoint"]

    # Gather forecast summary information for the next two days.

    forecasts = []
    for i in range(3):
        inspectionTime = int(time.time()) + 60*60*24*i
        wea_response = query_request("api.darksky.net",
                                     "/forecast/{key}/{latit},{longi},{tim}"
                                     .format(key=forecast_token,
                                             latit=lat,
                                             longi=lon,
                                             tim=inspectionTime
                                             )
                                     )

        print(wea_response["daily"]["data"][0]["summary"])
        forecasts.append(wea_response["daily"]["data"][0]["summary"])

    constructedString = ("The weather in **{city}** is **{temp}°F**"
                         "with **{hum}** humidity."
                         "The dewpoint is **{dew}**°F\n"
                         "\n"
                         "Today's forecast: {tf}\n"
                         "Tomorrow: {f1}\n"
                         "The day after: {f2}\n")

    # Output all of it
    return constructedString.format(city=cityName,
                                    temp=weather_f,
                                    dew=dewpoint,
                                    hum=humidity,
                                    f1=forecasts[0],
                                    f2=forecasts[1],
                                    tf=forecasts[2])
