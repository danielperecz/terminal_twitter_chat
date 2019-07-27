from logging.config import dictConfig
from platform import system
import logging
import twitter
import yaml
import sys
import os


# Using this variable ensures paths are cross platform
slash = "\\" if system() is "Windows" else "/"

# Configure logger
dictConfig(yaml.safe_load(open(os.path.abspath("..") + slash + "config.yaml")))


class TwitterTerminalChat:

    logger = logging.getLogger("chat.py")

    def __init__(self):
        self.logger.info("Initialising TwitterTerminalChat()")

        # Get keys & tokens from text file
        account = self.read_account()
        if account is False:
            self.logger.error("Invalid account.txt")
            sys.exit()

        self.consumer_key = account[0]
        self.consumer_secret = account[1]
        self.access_token_key = account[2]
        self.access_token_secret = account[3]

        # Initialize an Api object
        try:
            self.api = twitter.Api(self.consumer_key, self.consumer_secret,
                                   self.access_token_key, self.access_token_secret)
            self.api.VerifyCredentials()
        except:
            self.logger.error("Invalid key(s) and or token(s) in account.txt")
            sys.exit()

        self.logger.info("Successfully initialised TwitterTerminalChat()")

    def read_account(self):
        with open(os.path.abspath("..") + slash + "account.txt", "r") as f:
            lines = f.read().splitlines()
            if len(lines) == 4:
                return lines
        return False


TwitterTerminalChat()
