# voight-kampff

Inspired by the robotic testing system from "Do Andoirds Dream of Electric Sheep", this small discord bot sits around and accomplishes some simple commands.

To install, it's important to have a python file called `lorem.py` which has the following variables defined as string literals:
* `discord_token` - Api key given by discord
~~* `wunder_token` - wunderground weather token~~ **Deprecated due to API closing**
* `location_token` - Using *locationiq* geocoding API
* `forecast_token` - Using *forecast.io* weather API

Currently `discord.py` only supports python 3.4-3.6 due to `async` support.

***Note:*** This is an active project with many features unimplemented or to be improved.
