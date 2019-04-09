import logging 

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def general_log(message):
    logger.info(message)

def command_log_info(user, command_name, command_details):
    logger.info(user + 
                " requested " + 
                command_details + 
                " from " + 
                command_name
                )
