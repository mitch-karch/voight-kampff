from discord import Embed
from helper_functions.logger import error_debug

errorSymbol = "https://i.imgur.com/fgZ5XzG.png"


def errorEmbedBuilder(error_message, origin_function, error_colour=0xFF9494):
    em = Embed(
        title=origin_function + " Error", description=error_message, colour=error_colour
    )
    em.set_thumbnail(url=errorSymbol)
    error_debug(origin_function, error_message)
    return em
