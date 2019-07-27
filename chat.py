import twitter


class TwitterTerminalChat:

    def __init__(self, consumer_key, consumer_secret, access_token_key, access_token_secret):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token_key = access_token_key
        self.access_token_secret = access_token_secret

        # Initialize an Api object
        self.api = twitter.Api(self.consumer_key, self.consumer_secret, self.access_token_key, self.access_token_secret)


if __name__ == "main":
    TwitterTerminalChat(consumer_key="-",
                        consumer_secret="-",
                        access_token_key="-",
                        access_token_secret="-")
