import spotipy
import spotipy.oauth2 as oauth2
from spotipy.oauth2 import SpotifyClientCredentials
import json
import spotipy.util as util
#from json.decoder import JSONDecodeError
from json import decoder
import os
import sys
import webbrowser
import socket
import pprint
import subprocess
import requests


username = "jason_faul?si=CWQ1OXmNTRqZcWDz2PHTVg"
CLIENT_ID = '3010fefedd7c4c939a073b44323ff568'
CLIENT_SECRET = '3cfc29bdba1b47579982da6b8139938a'
REDIRECT_URI='https://developer.spotify.com/'
SCOPE = 'playlist-modify-public playlist-read-private playlist-read-collaborative'

#creates spotify object
def createSpotifyObject():
    credentials = oauth2.SpotifyClientCredentials(
        client_id=CLIENT_ID,client_secret=CLIENT_SECRET)
    token = credentials.get_access_token()
    spotifyObject = spotipy.Spotify(auth=token)
    return spotipy.Spotify(auth=token)

#gets id for a specific track
def getTrackID(title, artist, spotifyObject):
    result = spotifyObject.search("artist:" + artist + " track:" + title,1,0)
    spotifyID = result['tracks']['items'][0]['id']
    #print(json.dumps(spotifyID, sort_keys = True, indent = 4))
    return(spotifyID)

#gets cover art based on title and artist
def showCoverArt(title, artist, spotifyObject):
    result = spotifyObject.search("artist:" + artist + " track:" + title,1,0, 'track')
    trackArt = result['tracks']['items'][0]['album']['images'][0]['url']
    #print(json.dumps(trackArt, sort_keys = True, indent = 4))
    return (trackArt) #url
    #webbrowser.open(trackArt)

'''
def showCoverArt(track_id, spotifyObject):
    #The function takes in the track id of a song, and
        #returns the cover art of the album.
    track = spotifyObject.track(track_id)
    trackArt = track['album']['images'][0]['url']
    #webbrowser.open(trackArt)
    return (trackArt) #url
'''

def listen(title, artist, spotifyObject):
    ''' Takes in the title and artist of a song, and opens
        Spotify's web browser to play the song.'''
    track = spotifyObject.search("artist:" + artist + " track:" + title,1,0, 'track')
    #print(json.dumps(track, sort_keys = True, indent = 4))
    #openTrack = track['tracks']['items'][0]['external_urls']['spotify'] ORIGINAL
    openTrack = track['tracks']['items'][0]['uri']
    return (openTrack)
    #webbrowser.open(openTrack)


'''def listen(track_id, spotifyObject):
        Takes in the track id of a song, and opens
        Spotify's web browser to play the song.
    track = spotifyObject.track(track_id)
    openTrack = track['external_urls']['spotify']
    return(openTrack)
    #webbrowser.open(openTrack)
'''

def songsFromLastFM(nestedList, spotifyObject):
    '''The function takes in the nested list of recommended
        songs [['artist1','songTitle1'],[['artist2','songTitle2'],...]
        and returns a list of the trackIDs for each song.'''
    recommendedSongs = []
    for list1 in nestedList:
        songArtist = list1[0]
        songTitle = list1[1]
        track_id = getTrackID(songTitle, songArtist, spotifyObject)
        recommendedSongs.append(track_id)
    return(recommendedSongs)

'''
if __name__ == '__main__':
    spotifyObject = createSpotifyObject()
    searchTitle = "Good Morning"
    searchArtist = "Kanye West"
    print(listen(searchTitle, searchArtist, spotifyObject))

    for key in musicDict:
        print("\n"+key+"\n")
        for list in musicDict[key]:
            print(list[1] + " by " + list[0])
            showCoverArt(list[1],list[0],spotifyObject)

'''
