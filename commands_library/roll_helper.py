import logging
import random
import re
from discord import Embed

SimpleDiceRe = re.compile(r"d?(\d+)")


def get_range_from_spec(spec):
    if spec == "":
        return [0, 1]
    m = SimpleDiceRe.search(spec)
    if m:
        upper = int(m.group(1))
        return [1, upper]
    return [1, 2]


def roll_generator(dice_spec):
    r = get_range_from_spec(dice_spec)
    return random.randint(*r)


def roll_helper(dice_spec):
    message = roll_generator(dice_spec)
    return Embed(title="Dice roll:" + dice_spec, description=message, colour=0xFFFF00)


if __name__ == "__main__":
    print(roll_generator(""))
    print(roll_generator("d2"))
    print(roll_generator("d20"))
    print(roll_generator("20"))
