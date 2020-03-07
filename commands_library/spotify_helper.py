from discord import Embed

from commands_library.query_helper import query_request, payload_post

from helper_functions.logger import general_debug, general_info
from helper_functions.errorHelpers import errorEmbedBuilder

def spotify_on_message_hook(channel, message):
    print(channel)
    print(message)

if __name__ == "__main__":
    pass
