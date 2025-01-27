import os
import json
import logging
from config import Config
import process

# Global Logger
logging.basicConfig(filename='app.log', filemode='a',
                    format='%(asctime)s - %(name)-20s - %(levelname)s - %(message)s', level=logging.DEBUG,encoding='utf-8')
logger = logging.getLogger("app")

# Global Data - App Config
app_config = None


def LoadConfig():

    CONFIGURATION_FILE = "appconfig.json"
    try:
        with open(CONFIGURATION_FILE, "r", encoding='utf-8') as jsonfile:
            cfg = json.load(jsonfile)
            logger.info(
                f'Success loading configuration file {CONFIGURATION_FILE}') #: {cfg}')
            return True, cfg
    except Exception as e:
        print("An exception occurred:", e)
        logger.error(
            f'Error loading configuration file {CONFIGURATION_FILE}, {e}')
        return False, None



# Defining main function
def main():
    
    global app_config
    
    logger.info("Application started")
    # Load configuration
    success, cfg = LoadConfig()
    if (not success):
        logger.error("App Configuration was not loaded. The process cannot continue.")    
    else:
        # Make an instance of Config class global
        app_config = Config(cfg)

        # Main process
        process.start(app_config)

    logger.info("Application finished")

# Main
if __name__ == "__main__":
    main()
