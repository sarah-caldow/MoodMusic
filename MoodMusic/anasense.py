import tweepy
import json
from MoodMusic import keys
from datetime import datetime
from datetime import timedelta

def getTweets():
    user = '@MatthewMercer'
    tweets = []
    #set range of tweet time from now to x hours before now 
    timerange = 12;

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
            
#if __name__ == '__main__':
#    tweets = getTweets()
#    for tweet in tweets:
#        print(tweet.text.encode("utf-8", errors="replace"))

