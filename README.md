# Twitter Terminal Chat [WIP]
## Goal
Be able to chat with anyone via a terminal on any Operating System.

## Progress
[Progress Tracker](https://github.com/danielperecz/twitter_terminal_chat/projects/1)
### So far:
* The class `TwitterTerminalChat` reads user information from `account.txt` and its `__init__` method initialises a tweepy `API` object using this information.
* 2 way communication is now possible but it takes a long time to get an updated list of new direct messages (60+ seconds). This seems to be a limitation of the underlying Twitter API itself. Currently I'm retrieving direct messages using: `tweepy.API().list_direct_messages()`.

### What's next:
* Improving the communication speed

## Demo
Here's how it looks like in a terminal.
* The green text is your input (it's green due to PyCharm IDE).
* First you type in the Twitter account (note it's the name that starts with @).
* Once you have entered the account name, the last message within a certain period of time, from that user, will be displayed on the next line.
* You can now enter input.
* The keyword to stop the script is `exit`.
![screenshot](https://i.imgur.com/lAiSJAF.png)

## Current imports (will be automated)
```python
from logging.config import dictConfig
from platform import system
import threading
import logging
import tweepy
import queue
import yaml
import sys
import os
```
