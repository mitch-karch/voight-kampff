from discord import Embed
from commands_library.query_helper import query_request
from helper_functions.logger import general_debug, general_info
from helper_functions.errorHelpers import errorEmbedBuilder


def websterDict_helper(request_word, api_key, max_definitions=5):
    if len(request_word.split(" ")) > 1:
        request_word = request_word.replace(" ", "%20")

    data = query_request(
        "www.dictionaryapi.com",
        "/api/v3/references/collegiate/json/{t}?key={k}".format(
            t=request_word, k=api_key
        ),
    )
    if not any(isinstance(x, dict) for x in data):
        return errorEmbedBuilder(
            "Couldn't define: *"
            + request_word
            + "* "
            + "did you mean: "
            + ", ".join(data),
            "Webster Dictionary",
        )

    general_debug("Webster Dictionary is: " + str(data))

    em = Embed(title="Webster Dictionary: " + data[0]["meta"]["id"], colour=0x2784EF)

    for element in range(min(max_definitions, len(data))):
        datum = data[element]
        em.add_field(
            name=datum["meta"]["id"] + "(" + datum["fl"] + ")",
            value=";\n".join(datum["shortdef"]),
            inline=False,
        )

    general_info("Webster Dictionary created and returned embed object")
    return em
