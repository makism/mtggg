import sys
import tweepy as tw

consumer_key = "KF2af8ed1Mpf4f10VaSZvkL1b"
consumer_secret = "FNJRTvMzPJMtLLwNO1mrrNH9fu1Ky1GwetEAikEFAKnDfCk1Sm"
access_token = "1150333679224459265-bjNjocxNLlrxpWA1DooZ3vbemPgF4j"
access_token_secret = "iI3HsrjAKpCNJ8zfcBpHAoRH1i1KiYCjzY6qPH06fs3fc"

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
