# Twitter Terminal Chat [WIP]
## Goal
Be able to chat with anyone via a terminal on any Operating System.

## How it works
### So far:
* The class `TwitterTerminalChat` reads user information from `accounts.txt` and its `__init__` method initialises a tweepy `API` object using this information.
* 2 way communication is now possible but it takes a long time to get an updated list of new direct messages (around 20 seconds). This seems to be a limitation of the API itself. Currently I'm retrieving direct messages using: `tweepy.API().list_direct_messages()`.

### What's next:
* Improving the communication speed

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
