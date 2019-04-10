from discord import Embed
from commands_library.query_helper import query_request
from helper_functions.logger import general_debug, general_info


def urbanDict_helper(request_definition, char_lim=1000):
    if(len(request_definition.split(" ")) > 1):
        request_definition = request_definition.replace(" ", "%20")

    data = query_request("api.urbandictionary.com",
                         "/v0/define?term={stk}".format(stk=request_definition)
                         )

    definitions = data["list"]

    general_debug("Urban Dictionary is: " + str(definitions[0]))

    temp_defn = definitions[0]["definition"]
    temp_example = definitions[0]["example"]

    if len(temp_defn) > char_lim:
        temp_defn = definitions[0]["definition"][:char_lim] + "__[truncated]__"

    if len(temp_example) > char_lim:
        temp_example = definitions[0]["example"][:char_lim] + "__[truncated]__"

    em = Embed(title="Urban Dictionary: " + definitions[0]["word"],
               colour=0xef8427
               )
    em.add_field(name="Definition",
                 value=temp_defn
                 )
    em.add_field(name="Example",
                 value="*" + temp_example+ "*"
                 )

    general_info("Urban Dictionary created and returned embed object")
    return em
