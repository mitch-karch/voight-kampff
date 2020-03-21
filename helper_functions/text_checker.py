import json
import random


response_library = []


def response_init():
    global response_library
    with open("responseDict.json", "r", encoding="utf8") as f:
        response_library = json.load(f)


def dictionary_lookup(givenPhrase):
    for entry in response_library:
        if givenPhrase.lower().find(entry["word"]) != -1:
            rollValue = random.uniform(0, 1)
            if entry["probability"] > rollValue:
                return entry["response"]
            return False
    return False
