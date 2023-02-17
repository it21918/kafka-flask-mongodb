import snscrape.modules.twitter as sntwitter
import pandas as pd

def get_tweets(word, limit=100, until="2023-01-01", since="2020-01-01"):
    if word is not None :
        query = "(" + word + ")" + "until:" + until + "since:" + since
        tweets = ''
        limit = limit
        index = 0


        for tweet in sntwitter.TwitterSearchScraper(query).get_items():
            if limit == index:
                break
            else:
                tweets = str(tweet.rawContent) + '\n' + str(tweets)
            index = index + 1

        # to save to csv
        # df.to_csv('tweets.csv')
        return tweets
    return None