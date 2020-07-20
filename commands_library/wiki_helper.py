from discord import Embed
from commands_library.query_helper import query_request
from helper_functions.logger import general_debug, general_info
from helper_functions.errorHelpers import errorEmbedBuilder


def wiki_helper(request_word, char_lim=900):
    if len(request_word.split(" ")) > 1:
        request_word = request_word.replace(" ", "%20")

    data = query_request(
        "en.wikipedia.org",
        "/w/api.php?action=opensearch&search={t}"
        "&limit=1&namespace=0&format=json".format(t=request_word),
    )
    print(data)
    print(type(data))
    if not any(isinstance(x, list) for x in data):
        return errorEmbedBuilder(
            "Couldn't wikifind: *" + request_word + "* ", "Wikipedia Entry"
        )

    general_debug("Wikipedia Entry is:" + str(data))

    data2 = query_request(
        "en.wikipedia.org",
        "/w/api.php?action=query&titles={t}"
        "&prop=extracts&exintro&explaintext&format=json".format(
            t=data[1][0].replace(" ", "%20")
        ),
    )

    message = (
        "[{0}]({1}):\n".format(data[1][0], data[3][0])
        + data2["query"]["pages"][list(data2["query"]["pages"].keys())[0]]["extract"]
    )

    message = length_limiter(message, char_lim)

    em = Embed(
        title="Wikipedia Entry: " + data[1][0], colour=0xFFE9AB, description=message
    )

    general_info("Wikifind created and returned embed object")
    return em

def length_limiter(givenString, char_lim):
    if len(givenString) > char_lim:
        return givenString[:char_lim] + " __***|Truncated Definition|***__"
    return givenString
