import http.client
import json

headers = {
    'cache-control': "no-cache",
}

def urbanDict_helper(request_definition):
    char_lim=1000
    if(len(request_definition.split(" ")) > 1):
        request_definition = request_definition.replace(" ","%20")

    conn = http.client.HTTPSConnection("api.urbandictionary.com")
    conn.request("GET", "/v0/define?term={stk}".format(stk=request_definition), headers=headers)
    json_response = json.loads(conn.getresponse().read().decode("utf-8"))
    definitions = json_response["list"]
    print(definitions[0]["definition"]);

    print("Urban Dictionary is:" + definitions[0]["word"])
    constructedString = ("__Urban Dictionary: ***{full}***__\n"
                        "\n"
                        "{defn}\n"
                        "*{example}*"
                        )
    return constructedString.format(
            defn=(definitions[0]["definition"][:char_lim] + "__[truncated]__") if len(definitions[0]["definition"]) > char_lim else definitions[0]["definition"], 
            full=definitions[0]["word"], 
            example=(definitions[0]["example"][:char_lim] + "__[truncated]__") if len(definitions[0]["example"]) > char_lim else definitions[0]["example"], 
            )
                    

