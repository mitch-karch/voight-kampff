from commands_library.query_helper import query_request

headers = {
    'cache-control': "no-cache",
}


def urbanDict_helper(request_definition, char_lim=1000):
    if(len(request_definition.split(" ")) > 1):
        request_definition = request_definition.replace(" ", "%20")

    data = query_request("api.urbandictionary.com",
                         "/v0/define?term={stk}".format(stk=request_definition)
                         )

    definitions = data["list"]

    print("Urban Dictionary is:" + definitions[0]["word"])
    constructedString = ("__Urban Dictionary: ***{full}***__\n"
                         "\n"
                         "{defn}\n"
                         "*{example}*"
                         )

    temp_defn = definitions[0]["definition"]
    if len(temp_defn) > char_lim:
        temp_defn = definitions[0]["definition"][:char_lim] + "__[truncated]__"

    temp_example = definitions[0]["example"]
    if len(temp_example) > char_lim:
        temp_example = definitions[0]["example"][:char_lim] + "__[truncated]__"
    return constructedString.format(
            defn=temp_defn,
            full=definitions[0]["word"],
            example=temp_example,
            )
