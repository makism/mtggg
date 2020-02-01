import sys
import tweepy as tw
from pymongo import MongoClient
from json import loads


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


if __name__ == "__main__":
    mongo_client = MongoClient("localhost:27017")
    collection = mongo_client.mtg_tweets.all

    consumer_key = "KF2af8ed1Mpf4f10VaSZvkL1b"
    consumer_secret = "FNJRTvMzPJMtLLwNO1mrrNH9fu1Ky1GwetEAikEFAKnDfCk1Sm"
    access_token = "1150333679224459265-bjNjocxNLlrxpWA1DooZ3vbemPgF4j"
    access_token_secret = "iI3HsrjAKpCNJ8zfcBpHAoRH1i1KiYCjzY6qPH06fs3fc"

    auth = tw.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tw.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

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
        "#MTGTheros",
    ]

    tags = " OR ".join(tags)

    for tweet in tw.Cursor(
        api.search,
        q=tags,
        count=10,
        lang="en",
        since="2019-01-01",
        tweet_mode="extended",
    ).items():
        collection.insert_one(tweet._json)
        print(". ", end="")

    print("Done .")
