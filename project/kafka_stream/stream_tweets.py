import sys
import tweepy as tw

# Fetch the credentials from the secrets file.
consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""

auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


class Listener(tw.streaming.StreamListener):
    def __init__(self):
        super(Listener, self).__init__()

    def on_status(self, status):
        print(status.text)
        print()

    def on_error(self, status_code):
        if status_code == 420:
            # returning False in on_data disconnects the stream
            return False


listener = Listener()
stream = tw.Stream(auth=api.auth, listener=listener)

tags = [
    "#MTGArena",
    "#mtga",
    "#mtg",
    "#magicthegathering",
    "#mtgcommunity",
    "#mtgaddicts",
    "#mtgmemes",
    "#mtgspoilers",
    "#mtgmodern",
]

try:
    print("Start streaming...")
    stream.filter(track=tags)
except KeyboardInterrupt:
    print("Stopped.")
finally:
    print("Done.")
    stream.disconnect()
