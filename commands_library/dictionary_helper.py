from discord import Embed
from commands_library.query_helper import query_request
from helper_functions.logger import general_debug, general_info
from helper_functions.urlBuilder import urlBuilder


def urbanDict_helper(request_definition, char_lim=1000):
    if(len(request_definition.split(" ")) > 1):
        request_definition = request_definition.replace(" ", "%20")

    data = query_request("api.urbandictionary.com",
                         "/v0/define?term={stk}".format(stk=request_definition)
                         )

    definitions = data["list"]

    general_debug("Urban Dictionary is: " + str(definitions[0]))

    temp_def = definitions[0]["definition"]
    temp_example = definitions[0]["example"]

    temp_def = length_limiter(temp_def, char_lim)
    temp_example = length_limiter(temp_example, char_lim)

    em = Embed(title="Urban Dictionary: " + definitions[0]["word"],
               url=definitions[0]["permalink"],
               colour=0xef8427
               )
    em.add_field(name="Definition",
                 value=temp_def
                 )
    em.add_field(name="Example",
                 value="*" + temp_example + "*"
                 )

    general_info("Urban Dictionary created and returned embed object")
    return em


def urbanDict_multiple(request_definition, numberOfDefs=3, char_lim=1000):

    if(len(request_definition.split(" ")) > 1):
        request_definition = request_definition.replace(" ", "%20")

    data = query_request("api.urbandictionary.com",
                         "/v0/define?term={stk}".format(stk=request_definition)
                         )

    definitions = data["list"]

    em = Embed(title="Urban Dictionary Top "+str(numberOfDefs)+": "
                     + definitions[0]["word"],
               colour=0xef8427
               )

    definitionRange = min(numberOfDefs, len(definitions))
    for defin in range(definitionRange):

        temp_def = length_limiter(definitions[defin]["definition"], char_lim)
        temp_example = length_limiter(definitions[defin]["example"], char_lim)
        em.add_field(name="Definition "+str(defin+1),
                     value=urlBuilder(temp_def,definitions[defin]["permalink"])
                     )
        em.add_field(name="Example "+str(defin+1),
                     value="*" + temp_example + "*"
                     )

        if(defin != definitionRange-1):
            emptyString = "\u200B "
            em.add_field(name=emptyString,
                         inline=False,
                         value=emptyString
                         )

    return em


def length_limiter(givenString, char_lim):
    if len(givenString) > char_lim:
        return givenString[:char_lim] + "__[truncated]__"
    return givenString
