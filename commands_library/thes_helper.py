from discord import Embed
from commands_library.query_helper import query_request
from helper_functions.logger import general_debug, general_info
from helper_functions.errorHelpers import errorEmbedBuilder


def thes_helper(request_word, api_key, max_definitions=7):
    if len(request_word.split(" ")) > 1:
        request_word = request_word.replace(" ", "%20")

    data = query_request(
        "www.dictionaryapi.com",
        "/api/v3/references/thesaurus/json/{t}?key={k}".format(
            t=request_word, k=api_key
        ),
    )
    if not any(isinstance(x, dict) for x in data):
        return errorEmbedBuilder(
            "Couldn't thesaurus: *"
            + request_word
            + "* "
            + "did you mean: "
            + ", ".join(data),
            "Webster Thesaurus",
        )

    general_debug("Thesaurus lookup is: " + str(data))

    syns = data[0]["meta"]["syns"][0]

    number_of_entries = min(len(syns),max_definitions)

    em = Embed(
        title="Thesaurus Entry: " + data[0]["meta"]["id"],
        colour=0xEDBE47,
        description=", ".join(syns[:number_of_entries]),
    )

    general_info("Thesaurus Lookup created and returned embed object")
    return em
