import random
import uuid
from helper_functions.logger import general_debug, general_info
from discord import Embed


def random_helper(commandType, value):
    message = ""
    if commandType == "Roll ":
        message = "You rolled a: "
        message += str(randomNumber(value))
    elif commandType == "UUID":
        value = ""
        message = randUUID()

    em = Embed(title=commandType + str(value), description=message, colour=0xFFFF00)

    return em


def randomNumber(maxValue):
    if maxValue < 2:
        maxValue = 2
    return random.randint(1, maxValue)


def randUUID():
    return uuid.uuid4().hex
