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
    try:
        #os.remove(".cache-{}".format(username))
        #os.remove(f".cache-{username}")
        token = util.prompt_for_user_token(username = username, scope = SCOPE, client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI)
    except (AttributeError, decoder.JSONDecodeError):
        #os.remove(".cache-{}".format(username))
        token = util.prompt_for_user_token(username = username, scope = SCOPE, cclient_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI)   

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
    print ("opening browser")
    webbrowser.open(trackArt)

if __name__ == '__main__':

    spotifyObject = createSpotifyObject()
    ###Get Track id 
    searchTitle = "Good Morning"
    searchArtist = "Kanye West"    
    track_id = getTrackID(searchTitle,searchArtist, spotifyObject)

    ### Shows the cover art by opening a browser
    showCoverArt(searchTitle, searchArtist, spotifyObject)