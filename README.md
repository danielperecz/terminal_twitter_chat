# Terminal Twitter Chat [WIP]
## Goal
Be able to chat with anyone via a terminal on any Operating System.

## How it works
### So far:
The class `TerminalTwitterChat` reads user information from `accounts.txt` and its `__init__` method initialises a Twitter `Api` object using this information.

### What's next:
Using the `Api` object I will implement the Direct Message feature.

## Currently working on
* Implementing a way to get new messages received. The API can do this but it's rate limited so I've decided to use Selenium's Chrome object for detecting new messages
* At the moment the script logs in to Twitter and goes to specific chat window
* Next is the implementation of detecting new messages
* Will have to use multithreading because this 'listener' method will have to listen to new messages while at the same time the user should have the ability to send a new message

## Dependencies (will be automated)
```
selenium
tweepy
yaml
pyyaml
```
