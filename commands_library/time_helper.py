import time
import pytz

from discord import Embed

from helper_functions.logger import general_debug, general_info

def time_helper(query):
    em = Embed(title="time", description=query, colour=0xFFFF00)
    return em

if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
