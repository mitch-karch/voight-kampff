from discord import Embed
from commands_library.query_helper import query_request, payload_request
from helper_functions.logger import general_debug, general_info
from helper_functions.errorHelpers import errorEmbedBuilder


def wiki_helper(request_word):
    if len(request_word.split(" ")) > 1:
        request_word = request_word.replace(" ", "_")

    data = payload_request(
        "https://en.wikipedia.org/api/rest_v1/page/summary/{t}?redirect=true&origin=*".format(
            t=request_word
        ),
    )
    general_debug("Wikipedia Entry is:" + str(data))

    message = length_limiter(data["extract"])

    em = Embed(
        title="Wikipedia Entry:" + data["title"],
        url=data["content_urls"]["desktop"]["page"],
        colour=0xFFE9AB,
        description=message,
    )

    if "thumbnail" in data:
        em.set_thumbnail(url=data["thumbnail"]["source"])

    general_info("Wikifind created and returned embed object")
    return em

def length_limiter(givenString, char_lim=900):
    if len(givenString) > char_lim:
        return givenString[:char_lim] + " __***|Truncated Definition|***__"
    return givenString