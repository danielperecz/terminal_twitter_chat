from logging.config import dictConfig
from platform import system
import logging
import tweepy
import yaml
import sys
import os


# Using this variable ensures paths are cross platform
slash = "\\" if system() is "Windows" else "/"

# Configure logger
dictConfig(yaml.safe_load(open(os.path.abspath("..") + slash + "config.yaml")))


class TwitterTerminalChat:

    logger = logging.getLogger("chat.py")

    api = None
    my_id = None

    def __init__(self):
        self.logger.info("Initialising TwitterTerminalChat()")

        # Get keys & tokens from text file
        account = self.read_account()
        if account is False:
            self.logger.error("Invalid account.txt")
            sys.exit()

        # Initialise keys & tokens from text file
        self.consumer_key = account[0]
        self.consumer_secret = account[1]
        self.access_token_key = account[2]
        self.access_token_secret = account[3]

        # Authenticate user, setup api, and verify whether successful
        try:
            self.auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
            self.auth.set_access_token(self.access_token_key, self.access_token_secret)
            self.api = tweepy.API(self.auth)
            self.api.verify_credentials()
        except:
            # If unsuccessful verify_credentials() causes an exception
            self.logger.error("Invalid key(s) and or token(s) in account.txt")
            sys.exit()

        self.my_id = self.api.verify_credentials()._json["id"]
        self.open_chat()
        self.logger.info("Successfully initialised TwitterTerminalChat()")

    def read_account(self):
        """Method reads account.txt and returns its contents as a list of lines."""
        with open(os.path.abspath("..") + slash + "account_.txt", "r") as f:
            lines = f.read().splitlines()
            if len(lines) == 4:
                return lines
        return False

    def open_chat(self):
        """This method is responsible for the actual chatting feature. User is prompted for a recipient username and
        then they may start chatting."""

        # Prompt user to enter a recipient username
        recipient_username = input("\nOpen chat with: ")
        if recipient_username.lower() == "exit":
            sys.exit()

        # Get recipient's ID
        try:
            recipient_id = self.api.get_user(screen_name=recipient_username)._json["id"]
        except:
            # User not found. Call open_chat() again to prompt user for new username
            self.logger.error("User not found")
            self.open_chat()

        message = input(">>> ")

        # Keep prompting user for new input until "exit" is entered
        while message.lower() != "exit":
            self.api.send_direct_message(recipient_id=recipient_id, text=message)       # Send message
            message = input(">>> ")                                                     # Prompt user for new message

        # "exit" has been entered therefore stop code execution
        sys.exit()


TwitterTerminalChat()

"""
Notes for myself:
listing direct messages is rate limited

latest_message = self.api.list_direct_messages()[0].message_create["message_data"]["text"]
sender_id = self.api.list_direct_messages()[0].message_create["sender_id"]
"""
