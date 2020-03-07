import logging
import random
import re

SimpleDiceRe = re.compile(r'd(\d+)')

def get_range_from_spec(spec):
    if spec == "": return [0, 1]
    m = SimpleDiceRe.search(spec)
    if m:
        upper = int(m.group(1))
        return [1, upper]
    return [1, 2]

def roll_helper(dice_spec):
    r = get_range_from_spec(dice_spec)
    return random.randint(*r)

if __name__ == "__main__":
    print(roll_helper(""))
    print(roll_helper("d2"))
    print(roll_helper("d20"))
