from commands_library.query_helper import payload_request, query_request
from discord import Embed
import datetime
import time

weather_baseUrl = "https://darksky.net/forecast/"
details_baseUrl = "https://darksky.net/details/"
emojiDict = {'clear-day': '☀️',
             'clear-night': '🌙',
             'rain': '🌧️',
             'snow': '🌨️',
             'sleet': '☃️',
             'wind': '🍃',
             'fog': '🌫️',
             'cloudy': '☁️',
             'partly-cloudy-day': '⛅',
             'partly-cloudy-night': '☁️'
             }


def urlBuilder(text, link):
    return "["+text+"]("+link+")\n"


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
    humidity = '{:.1%}'.format(wea_response["currently"]["humidity"])
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

        tempObj = wea_response
        forecasts.append(tempObj)

    # mainUrl = weather_baseUrl + str(lat) + ',' + str(lon)
    detailsUrl = details_baseUrl + str(lat) + ',' + str(lon)

    # titleString = urlBuilder('__Forecast in ' + cityName + '__', mainUrl)
    mainString = ("It is currently **{temp}°F** "
                  "with **{hum}** humidity "
                  "and a dewpoint of **{dew}**°F\n"
                  ).format(temp=weather_f,
                           dew=dewpoint,
                           hum=humidity,
                           )
    # Output all of it
    em = Embed(title="Weather in " + cityName,
               description=mainString,
               colour=0x00FF00)

    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    dayAfter = today + datetime.timedelta(days=2)
    em.add_field(name="Today's forecast " + "(" +
                      str(forecasts[0]["daily"]["data"][0]["temperatureHigh"])
                      + "/"
                      + str(forecasts[0]["daily"]["data"][0]["temperatureLow"])
                      + "):",
                 value=emojiDict[forecasts[0]["daily"]["data"][0]["icon"]] +
                       urlBuilder(forecasts[0]["daily"]["data"][0]["summary"],
                                  detailsUrl + '/' + str(today)
                                  )
                 )

    em.add_field(name="Tomorrow's forecast " + "(" +
                      str(forecasts[1]["daily"]["data"][0]["temperatureHigh"])
                      + "/"
                      + str(forecasts[1]["daily"]["data"][0]["temperatureLow"])
                      + "):",

                 value=emojiDict[forecasts[1]["daily"]["data"][0]["icon"]] +
                       urlBuilder(forecasts[1]["daily"]["data"][0]["summary"],
                                  detailsUrl + '/' + str(tomorrow)
                                  )
                 )

    em.add_field(name="Day After's forecast " + "(" +
                      str(forecasts[2]["daily"]["data"][0]["temperatureHigh"])
                      + "/"
                      + str(forecasts[2]["daily"]["data"][0]["temperatureLow"])
                      + "):",

                 value=emojiDict[forecasts[2]["daily"]["data"][0]["icon"]] +
                       urlBuilder(forecasts[2]["daily"]["data"][0]["summary"],
                                  detailsUrl + '/' + str(dayAfter)
                                  )
                 )

    return em
