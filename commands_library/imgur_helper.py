from discord import Embed
from commands_library.query_helper import headers_request
from helper_functions.logger import general_debug, general_info
from helper_functions.errorHelpers import errorEmbedBuilder
from helper_functions.urlBuilder import urlBuilder


def imgur_top(req_image, imgur_id):
    headers = {
        'Authorization': 'Client-ID ' + imgur_id,
    }
    imgurUrl = 'https://api.imgur.com/3/gallery/search/viral/all?q_all={s}'.format(s=req_image)
    data = headers_request(imgurUrl,
                           headers 
                           )

    if len(data["data"]) == 0:
        return errorEmbedBuilder("Imgur couldn't find anything",
                                 "Imgur"
                                 )

    top_image = data["data"][0]

    em = Embed(title="Top image for " + req_image,
               description=urlBuilder(top_image["title"], top_image["link"]),
               colour=0x00FF00
               )
    if "images" in top_image.keys():
        em.set_image(url=top_image["images"][0]["link"])
    elif "link" in top_image.keys():
        em.set_image(url=top_image["link"])
    else:
        return errorEmbedBuilder("Imgur had issue with that request",
                                 "Imgur"
                                 )

    general_info("Imgur created and returned embed object")
    return em
