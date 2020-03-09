import json


responseLibrary = {}


def response_init():
    global responseLibrary
    with open("responseDict.json", "r", encoding="utf8") as f:
        responseLibrary = json.load(f)


def dictionary_lookup(givenPhrase):
    for k, v in responseLibrary.items():
        if k == givenPhrase:
            return v
    return False
