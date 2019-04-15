from discord import Embed
from commands_library.query_helper import query_request
from helper_functions.logger import general_debug, general_info

def string_formatter(given_s):
    if(len(given_s.split(" ")) > 1):
        given_s = given_s.replace(" ", "+")
    return given_s

def wolf_short_query(submit_q, w_token):
    fixed_request = string_formatter(submit_q)
    data = query_request("api.wolframalpha.com",
                         "/v1/result?appid={key}&i={r_s}".format(key=w_token,
                                                          r_s=fixed_request),
                         raw_return=True
                         )

    general_debug("Wolframalpha is: " + str(data))

    constructed_string = "**{question}?**\n" \
                         "*{answer}*".format(question=submit_q,
                                             answer=data
                                             )
    em = Embed(title="Wolfram Alpha",
               description=constructed_string,
               colour=0xF12223
               )

    general_info("Wolfram created and returned embed object")
    return em
