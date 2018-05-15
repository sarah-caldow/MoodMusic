import tweepy
import json
import random
from MoodMusic.application import keys
#from converted_dict import *
from datetime import datetime
from datetime import timedelta
from nltk.sentiment.vader import SentimentIntensityAnalyzer

musicDict = {'country_sad': [['Billy Joe Royal', 'Down in the Boondocks'], ['Miranda Lambert', 'Dead Flowers'], ['Miranda Lambert', 'Over You'], ['Vince Gill', 'Go Rest High On That Mountain'], ['Ryan Bingham', "Don't Wait For Me"], ['Mary Gauthier', 'Mercy Now'], ['Alan Jackson', 'Where Were You (When The World Stopped Turning)']], 'pop_chill': [['Mae', 'The Ocean'], ['Mazzy Star', 'Still Cold'], ['Michael Cretu', 'Mikado'], ['Burl Ives', 'Big Rock Candy Mountain'], ['Matt Costa', 'Behind The Moon'], ['The Bens', 'Bruised'], ['Pet Shop Boys', 'West End Girls'], ['Great Lake Swimmers', "River's Edge"], ['The Beautiful South', "I'll Sail This Ship Alone"]], 'rock_chill': [['Mae', 'The Ocean'], ['Mazzy Star', 'Still Cold'], ['Yo La Tengo', 'Something To Do'], ['The Herbaliser', 'Battle Of Bongo Hill'], ['Orange Goblin', 'Land Of Secret Dreams'], ['Echo And The Bunnymen', "I'll Fly Tonight"], ['Matt Costa', 'Behind The Moon'], ['Riverside', 'In Two Minds'], ['The Beautiful South', "I'll Sail This Ship Alone"]], 'rock_sad': [['Citizen Cope', "Son's Gonna Rise"], ['Gino Vannelli', 'Living Inside Myself'], ['Daughtry', 'Used To'], ['Okkervil River', 'A Favor'], ['Daughtry', "It's Not Over"], ['Riverside', 'Out Of Myself'], ['Billy Joe Royal', 'Down in the Boondocks']], 'hip-hop_happy': [['The Pussycat Dolls', 'Buttons'], ['Kelly Clarkson', 'Walk Away'], ['Rihanna', "Don't Stop The Music"], ['Gwen Stefani', 'Hollaback Girl'], ['RUN-DMC', "Run's House"], ['Groove Armada', 'At The River']], 'indie_sad': [['Orson', 'Look Around'], ['Natalie Walker', 'Colorblind'], ['Citizen Cope', "Son's Gonna Rise"], ['Daughtry', 'Used To'], ['Okkervil River', 'A Favor'], ['Daughtry', "It's Not Over"], ['Okkervil River', 'Get Big'], ['Amy Millan', 'I Will Follow You Into The Dark']], 'jazz_chill': [['Rx Bandits', 'Apparition'], ['The Herbaliser', 'Close Your Eyes'], ['Vanessa Da Mata', 'Case-se Comigo'], ['Dan Siegel', 'To The Point'], ["D'Angelo", 'When We Get By'], ['Bohren & Der Club Of Gore', 'Unkerich'], ['Charlie Parker', "Now's The Time"], ['Moca', 'Post It'], ['Dave Pike', 'Aphrodite']], 'country_happy': [['Creedence Clearwater Revival', 'Proud Mary'], ['Sugarland', 'Everyday America'], ['Johnny Cash', 'Jackson'], ['Shania Twain', "Don't Be Stupid (You Know I Love You)"], ['Creedence Clearwater Revival', 'Molina'], ['Brenda Lee', 'Rockin\x19 Around The Christmas Tree']], 'pop_sad': [['Ellie Goulding', 'The Writer'], ['Orson', 'Look Around'], ['Jordin Sparks', 'No Air'], ['Natalie Walker', 'Colorblind'], ['Daniele Silvestri', 'Mi Persi'], ['Citizen Cope', "Son's Gonna Rise"], ['Gino Vannelli', 'Living Inside Myself'], ['Craig David', 'Let Her Go']], 'jazz_happy': [['Charles Mingus', 'Better Git It In Your Soul'], ['Bah Samba', 'Reach Inside'], ['Barrio Jazz Gang', 'Chok-a-blok Avenue'], ['Positive Force', 'We Got The Funk'], ['Charlie Parker', 'Blues For Alice'], ['Horace Silver', 'Room 608'], ['Tony Allen', 'Home Cooking']], 'hip-hop_chill': [['The Herbaliser', 'Moon Sequence'], ['The Herbaliser', 'Close Your Eyes'], ['El-P', 'Time Wont Tell'], ['The Herbaliser', 'Battle Of Bongo Hill'], ['Jagged Edge', "Let's Get Married"], ['Funkdoobiest', 'Superhoes'], ['Kid Koala', 'Radio Nufonia'], ['The-Dream', 'Put It Down'], ['The Herbaliser', 'Goldrush']], 'pop_happy': [['Queen', 'We Will Rock You'], ['Queen', 'Bohemian Rhapsody'], ['Tahiti 80', 'Happy End'], ['La Casa Azul', 'El Sol No Brillará Nunca Más'], ['Dodgy', "If You're Thinking Of Me"], ['Positive Force', 'We Got The Funk'], ['Atlanta Rhythm Section', 'Spooky'], ['Middle Of The Road', 'Sacramento'], ['Mya', 'Now Or Never']], 'indie_happy': [['Sparklehorse', 'Someday I Will Treat You Good'], ['Dodgy', "If You're Thinking Of Me"], ['Matthew Good Band', 'Indestructible'], ['La Casa Azul', 'Siempre Brilla El Sol'], ['Tilly & The Wall', 'Brave Day'], ['Stephen Malkmus', 'Phantasies'], ['Mae', 'Futuro (Live)']], 'indie_chill': [['The Beautiful South', "I'll Sail This Ship Alone"], ['Mae', 'The Ocean'], ['Mazzy Star', 'Still Cold'], ['Neko Case', 'Hex'], ['Yo La Tengo', 'Something To Do'], ['Echo And The Bunnymen', "I'll Fly Tonight"], ['Matt Costa', 'Behind The Moon']], 'jazz_sad': [['Gino Vannelli', 'Living Inside Myself'], ['Louis Armstrong', "When It's Sleepy Time Down South"], ['Amy Winehouse', 'Tears Dry On Their Own'], ['Ella Fitzgerald', 'Miss Otis Regrets'], ['THE INK SPOTS', 'Into Each Life Some Rain Must Fall'], ['Katie Melua', 'I Cried For You']], 'country_chill': [['Neko Case', 'Hex'], ['Neko Case', 'Favorite'], ['Ryan Bingham', "Don't Wait For Me"], ['Willie Nelson', 'Angel Flying Too Close To The Ground'], ['Creedence Clearwater Revival', 'Bad Moon Rising'], ['Lynyrd Skynyrd', 'Sweet home Alabama'], ['Burl Ives', 'Big Rock Candy Mountain']], 'rock_happy': [['Queen', 'We Will Rock You'], ['Queen', 'Bohemian Rhapsody'], ['The Herbaliser', 'Battle Of Bongo Hill'], ['Sparklehorse', 'Someday I Will Treat You Good'], ['Dodgy', "If You're Thinking Of Me"], ['Positive Force', 'We Got The Funk'], ['Atlanta Rhythm Section', 'Spooky'], ['Middle Of The Road', 'Sacramento'], ['Matthew Good Band', 'Indestructible']], 'hip-hop_sad': [['Craig David', "My Love Don't Stop"], ['Natasha Bedingfield', 'Drop Me In The Middle'], ['Massive Attack', 'Unfinished Sympathy'], ['City High', 'What Would You Do?'], ['John Legend', "She Don't Have To Know"], ['Gwen Stefani', 'Cool'], ['2Pac', 'So Many Tears'], ['Girl Talk', 'All Eyes On Me']]}


#calculates an average sentiment for a list of tweets
def calculateAverageSentiment(sid, tweets):
    low = 10
    high = -10
    sum_sent = 0
    i = 0
    for tweet in tweets:
        sentiment = calculateSentiment(sid, tweet)
        if low > sentiment:
            low = sentiment
        if high < sentiment:
            high = sentiment
        sum_sent += sentiment
        i += 1
    avg = sum_sent/i
    return {"avg":avg, "low":low, "high":high}

#calculcates the sentiment score of the user to be used in music recommendation
def calculateSentiment(sid, tweet):
    ss = sid.polarity_scores(tweet)
    return ss["compound"];

#gets tweets from a certain user
def getTweets(timerange, num_tweets, user):
    tweets = []

    # Authenticate
    auth = tweepy.OAuthHandler(keys.consumer_key, keys.consumer_secret)
    auth.set_access_token(keys.access_token, keys.access_token_secret)

    api = tweepy.API(auth)
    tweets = api.user_timeline(screen_name = user, count = num_tweets, include_rts = False, tweet_mode='extended')

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

#removes links and videos from tweet
def stripTweet(tweet):
    words = tweet.split(" ")
    newword = []
    for word in words:
        if not('@' in word):
            if not('https://' in word):
                newword.append(word)
    strin = " ".join(newword)
    return strin

#determines sentiment of emotion tag sets
def determineTagMood(sid, tags):
    tagDict = {}
    for tag in tags:
        tagDict[calculateSentiment(sid, tag)] = tag
    return tagDict

#determines the baseline and unaltered mood and applies the baseline to the calculated mood
def determineMood(user):
    sid = SentimentIntensityAnalyzer()
    #moods = ["sad", "happy", "rage", "chill"]
    moods = ["sad", "happy", "chill"] #Without Rage
    baselineTweets = getTweets(168, 200, user)
    relevantMoodTweets = baselineTweets[:20]

    #find average range of moods, set mood words based on these emotions
    baseline = calculateAverageSentiment(sid, baselineTweets)
    unalteredMood = calculateAverageSentiment(sid, relevantMoodTweets)

    #print("Calculated Baseline:")
    #print(baseline["avg"])
    #print("Unaltered Mood:")
    #print(unalteredMood["avg"])

    #determine mood for user based on their baseline from the past week
    #set parameters of baseline
    mean = baseline["avg"]
    mood = unalteredMood["avg"] - mean
    radius = (abs(baseline["low"]) + abs(baseline["high"]))/2

    #if the only tweets made are the tweets included in the baseline
    if (baseline['avg'] == unalteredMood['avg']):
        mood = unalteredMood['avg']

    if (mood < 0 and mood < -radius):
        radius = -mood
    elif (mood > 0 and mood > radius):
        radius = mood

    #print("")
    #print("Adjusted Mood:")
    #print(mood)
    #print("High tweet:")
    #print(baseline['high'])
    #print("Low tweet:")
    #print(baseline['low'])
    #print("Calculated Radius:")
    #print(radius)

    #get sentiment score for tads
    unadjTags = determineTagMood(sid, moods)

    #normalize tags to new baseline
    tags = {}
    for tag in unadjTags:
        tags[tag/(radius*2)*1] = unadjTags[tag]

    #determine tag for user
    pic = min(tags, key=lambda x:abs(x-mood))

    #print("")
    #print("Nearest Sentiment:")
    #print(pic)
    #print("Nearest Tag:")
    #print(tags[pic])

    #return baseline #TO TEST BASELINE RATING
    return tags[pic]

#generate keys to access dictionary
def generateKeys(mood, genres):
    keys = []
    for genre in genres:
        keys.append(genre + "_" + mood)
    return keys

#generate random songs based on mood and several genres
def generateSongs(mood, genres):
    numSongs = 10
    keys = generateKeys(mood, genres)
    selected = []
    music = []
    for key in keys:
        music = music + musicDict[key]

    listSize = len(music)

    if(numSongs < listSize):
        for i in range(numSongs):
            selected.append(music.pop(random.randint(0, listSize-1))) #ERROR IF ONLY 1 GENRE SELECTED
            listSize -= 1
    else:
        for i in range(listSize):
            selected.append(music.pop(random.randint(0, listSize-1))) #ERROR IF ONLY 1 GENRE SELECTED
            listSize -= 1
    return selected
'''ORIGINAL
    for i in range(numSongs):
        selected.append(music.pop(random.randint(0, listSize-1))) #ERROR IF ONLY 1 GENRE SELECTED
        listSize -= 1
    return selected
'''


#def fixDictionary():
#    dictionary = {}
#    for key in musicDict.keys():
#        nug = musicDict[key]
#        row = []
#        j = 0
#        for i in nug:
#            a = list(nug[j][0][0])
#            j += 1
#            row.append(a)
#        dictionary[key] = row
#    print (dictionary)

#def fixDictionary2():
#    dictionary = {}
#    for key in musicDict.keys():
#        newNug = []
#        nug = musicDict[key]
#        while len(nug) != 0:
#            il = nug[0]
#            for j in range(1, len(nug)):
#                jl = nug[j]
#               if jl != il and jl not in newNug:
#                    newNug.append(nug[j])
#            nug.pop(0)
#        dictionary[key] = newNug
#    print (dictionary)

if __name__ == '__main__':
    user = '@HCI_Mood_Music'
    genres = ['hip-hop', 'country', 'jazz']

    sid = SentimentIntensityAnalyzer()
    moodTag = determineMood(user)
    print(moodTag)
    #for song in generateSongs(moodTag, genres):
        #print(song)
