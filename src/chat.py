from logging.config import dictConfig
from platform import system
import threading
import logging
import tweepy
import queue
import yaml
import sys
import os


# Using this variable ensures paths are cross platform
slash = "\\" if system() is "Windows" else "/"

# Configure logger
dictConfig(yaml.safe_load(open(os.path.abspath("..") + slash + "config.yaml")))


class TwitterTerminalChat:

    logger = logging.getLogger("chat.py")
    previous_messages = []
    refresh_time = 150000000
    message = None
    recipient_id = None
    recipient_nickname = None

    def __init__(self):
        self.logger.info("Initialising TwitterTerminalChat()")

        # Get keys & tokens from text file
        account = self.read_account()
        if account is False:
            self.logger.error("Invalid account.txt")
            sys.exit()

        # Initialise keys, tokens & twitter login details from text file
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
        self.logger.info("Successfully initialised TwitterTerminalChat()")
        self.open_chat()

    def read_account(self):
        """Method reads account.txt and returns its contents as a list of lines."""
        with open(os.path.abspath("..") + slash + "account.txt", "r") as f:
            lines = f.read().splitlines()
            if len(lines) == 4:
                return lines
        return False

    def message_listener(self):
        """Check for new messages and print them to terminal."""
        self.recipient_nickname = self.api.get_user(id=self.recipient_id)._json["name"]

        latest_messages = self.api.list_direct_messages()
        latest_messages_indexes = [i for i in range(0, len(latest_messages)) if
                                   int(latest_messages[i].message_create["sender_id"]) == self.recipient_id][::-1]
        sys.stdout.flush()
        for i in latest_messages_indexes:
            if latest_messages[i].message_create["message_data"]["text"] not in self.previous_messages:
                print(">>> " + self.recipient_nickname + ": " + latest_messages[i].message_create["message_data"]["text"])
                self.previous_messages.append(latest_messages[i].message_create["message_data"]["text"])

    def open_chat(self):
        """This method is responsible for the actual chatting feature. User is prompted for a recipient username and
        then they may start chatting."""

        # Prompt user to enter a recipient username
        recipient_username = input("\nOpen chat with: @")
        if recipient_username.lower() == "exit":
            sys.exit()

        # Get recipient's ID
        try:
            self.recipient_id = self.api.get_user(screen_name=recipient_username)._json["id"]
        except:
            # User not found. Call open_chat() again to prompt user for new username
            self.logger.error("User not found")
            self.open_chat()

        self.message_listener()

        input_queue = queue.Queue()
        input_thread = threading.Thread(target=self.wait_for_input_and_send, args=(input_queue,))
        input_thread.daemon = True
        input_thread.start()

        i = 0
        while True:
            if not input_queue.empty():
                self.previous_messages.append(input_queue.get())
            else:
                if i % self.refresh_time == 0:
                    self.message_listener()
            i += 1

        # "exit" has been entered therefore stop code execution
        sys.exit()

    def wait_for_input_and_send(self, input_queue):
        while True:
            sys.stdout.write(">>> ")
            self.message = sys.stdin.readline().strip()

            if self.message.lower() == "exit":
                sys.exit()

            self.api.send_direct_message(recipient_id=self.recipient_id, text=self.message)     # Send message
            input_queue.put(self.message)


TwitterTerminalChat()
