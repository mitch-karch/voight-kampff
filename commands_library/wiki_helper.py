from discord import Embed
from commands_library.query_helper import query_request
from helper_functions.logger import general_debug, general_info
from helper_functions.errorHelpers import errorEmbedBuilder


def wiki_helper(request_word):
    if(len(request_word.split(" ")) > 1):
        request_word = request_word.replace(" ", "%20")

    data = query_request("en.wikipedia.org",
                         "/w/api.php?action=opensearch&search={t}"
                         "&limit=1&namespace=0&format=json"
                         .format(t=request_word)
                         )
    if not any(isinstance(x, dict) for x in data):
        return errorEmbedBuilder("Couldn't wikifind: *" + request_word + "* ",
                                 "Wikipedia Entry"
                                 )

    general_debug("Wikipedia Entry is:" + str(data))

    data2 = query_request("en.wikipedia.org",
                          "/w/api.php?action=query&titles={t}"
                          "&prop=extracts&exintro&explaintext&format=json"
                          .format(t=request_word.replace(" ", "%20"))
                          )
    message = "[{0}]({1}):\n" + data2["query"]["pages"][0]["extract"]
    em = Embed(title="Wikipedia Entry: " + data[0][1],
               colour=0xffe9ab,
               description=message
               )

    general_info("Wikifind created and returned embed object")
    return em
