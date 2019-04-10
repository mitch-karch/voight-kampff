import json
import random

augLibrary = {"sakai": True}


def aug_finder(word):
    auWord = False
    if word in augLibrary:
        auWord = augLibrary[word]
    else:
        auWord = random.choice([True, False])
        augLibrary[word] = auWord
    with open('dict.json', 'w') as f:
        f.write(json.dumps(augLibrary))
    coinF = "is" if auWord else "is not"
    constructedString = "**{w}** __{c}__ aug und tier"

    general_debug("Aug und is: " + word + ":" + str(auWord))
    general_info("Returned Au definition")
    return constructedString.format(c=coinF, w=word)


def aug_init():
    global augLibrary
    with open('dict.json', 'r') as f:
        augLibrary = json.load(f)
