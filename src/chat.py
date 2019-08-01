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
    cpu_wait = 150000000
    message = None
    recipient_id = None
    recipient_nickname = None
    first_message_listener_call = True

    def __init__(self, account_txt_path=None):
        self.logger.info("Initialising TwitterTerminalChat()")
        self.account_txt_path = account_txt_path

        # Get keys & tokens from text file
        account = self.read_account()
        if account is False:
            self.logger.error("Invalid account.txt")
            sys.exit()

        # Initialise keys, tokens & twitter login details from text file
        self.consumer_key = account[0]
        self.consumer_secret = account[1]
        self.access_token = account[2]
        self.access_token_secret = account[3]

        # Authenticate user, setup api, and verify whether successful
        try:
            self.auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
            self.auth.set_access_token(self.access_token, self.access_token_secret)
            self.api = tweepy.API(self.auth)
            self.api.verify_credentials()
        except:
            # If unsuccessful verify_credentials() causes an exception
            self.logger.error("Invalid key(s) and or token(s) in account.txt")
            sys.exit()

        self.my_id = self.api.verify_credentials()._json["id"]
        self.logger.info("Successfully initialised TwitterTerminalChat()")

    def read_account(self):
        """Method reads account.txt and returns its contents as a list of lines."""
        path = self.account_txt_path if self.account_txt_path is not None else os.path.abspath("..") + slash + "account_.txt"
        with open(path, "r") as f:
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
        x = len(self.previous_messages)
        first_line = True
        for i in latest_messages_indexes:
            if self.first_message_listener_call:
                j = 0
                while j < len(latest_messages_indexes):
                    self.previous_messages.append(latest_messages[latest_messages_indexes[j]].message_create["message_data"]["text"])
                    j += 1
                sys.stdout.write(">>> " + self.recipient_nickname + ": " + latest_messages[latest_messages_indexes[-1]].message_create["message_data"]["text"] + "\n")
                self.first_message_listener_call = False
                return

            elif latest_messages[i].message_create["message_data"]["text"] not in self.previous_messages:
                if first_line:
                    sys.stdout.write(self.recipient_nickname + ": " + latest_messages[i].message_create["message_data"]["text"] + "\n")
                    first_line = False
                else:
                    sys.stdout.write(">>> " + self.recipient_nickname + ": " + latest_messages[i].message_create["message_data"]["text"] + "\n")
                self.previous_messages.append(latest_messages[i].message_create["message_data"]["text"])

        # If new messages have been received, they are written to terminal, but at the end a new blank line is started.
        # So instead of seeing ">>> ", the user only sees an empty line. This if statement fixes that problem.
        if x != len(self.previous_messages):
            sys.stdout.write(">>> ")

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

        # Call message_listener once to check for last message from the user you want to chat with
        self.message_listener()

        # Create a queue and a thread
        input_queue = queue.Queue()
        input_thread = threading.Thread(target=self.wait_for_input_and_send, args=(input_queue,))
        input_thread.daemon = True
        input_thread.start()

        i = 0
        while True:
            if not input_queue.empty():
                if self.message == "exit":
                    sys.exit()
                self.previous_messages.append(input_queue.get())
            else:
                # Check for new received messages every number of iterations specified by the cpu_wait variable
                if i % self.cpu_wait == 0:
                    self.message_listener()
            i += 1

    def wait_for_input_and_send(self, input_queue):
        """Runs simultaneously with the while loop in open_chat(). Method waits for user input and adds it to the queue,
        so it can then be used by open_chat()."""
        while True:
            sys.stdout.write(">>> ")
            self.message = sys.stdin.readline().strip()

            # If user wants to exit, we still need to add the string to the queue so the thread can be stopped from
            # the open_chat() method.
            if self.message.lower() == "exit":
                input_queue.put(self.message.lower())

            # Send direct message, and add it to queue so it can then be used outside of the thread.
            self.api.send_direct_message(recipient_id=self.recipient_id, text=self.message)
            input_queue.put(self.message)


if __name__ == "__main__":
    TwitterTerminalChat().open_chat()
