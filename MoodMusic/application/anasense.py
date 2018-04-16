import tweepy
import json
from MoodMusic.application import keys
from datetime import datetime
from datetime import timedelta
from nltk.sentiment.vader import SentimentIntensityAnalyzer

#calculates user emotional baseline based on tweets in the last month
def calculateBaseline(sid, tweets):
    
    return 0;

#calculcates the sentiment score of the user to be used in music recommendation
def calculateSentiment(sid, tweet):
    ss = sid.polarity_scores(tweet)
    return ss;

def getTweets(timerange, num_tweets):
    user = '@MatthewMercer'
    tweets = []

    # Authenticate
    auth = tweepy.OAuthHandler(keys.consumer_key, keys.consumer_secret)
    auth.set_access_token(keys.access_token, keys.access_token_secret)

    api = tweepy.API(auth)
    tweets = api.user_timeline(screen_name = user, count = 20, include_rts = False, tweet_mode='extended')

    #parses all tweets returned for tweets made between now and the specified timerange
    strtweets = []
    for status in tweets:
        now = datetime.now()
        dateposted = status.created_at
        timechange = now - dateposted
        if timechange.total_seconds() <= timerange*3600:
            strtweets.append(stripTweet(status.full_text));        
        else:
            break

    #returns list of relevant tweets
    return strtweets

def stripTweet(tweet):
    words = tweet.split(" ")
    newword = []
    for word in words:
        if not('@' in word):
            if not('https://' in word):
                newword.append(word)
    strin = " ".join(newword)
    return strin
            
if __name__ == '__main__':
    tweets = getTweets(6, 20)
    sid = SentimentIntensityAnalyzer()
    for tweet in tweets:
        print(tweet)
        print('{0}: {1}, '.format(k, ss[k]), end='')
        print()

