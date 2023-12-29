#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import urllib.parse
import json
import os
import time
import sys

FANART_API_KEY = "5081101fe9a223f58dc67aec86cdaf2e"


def get_musicbrainz_mbid(artist):
    """
        Get musicbrainz mbid for artist
        @param artist as str
        @return str
    """
    try:
        url = "http://musicbrainz.org/ws/2/artist/?query={}&fmt=json"
        url = url.format(urllib.parse.quote_plus(artist))
        # print(url)

        response = requests.get(url)
        if response.status_code == 200:
            json_data = response.json()
            if len(json_data["artists"]) == 0: 
                print ("{} : mbid non trouvé".format(artist))
                return None
            return json_data["artists"][0]["id"]
    except:
        # Logger.warning("MusicBrainz: %s", url)
        print("MusicBrainz exception : {}".format(url))
    return None

def get_fanarttv_artist_artwork_url(artist):
    """
        Get artist artwork using FanartTV
        @param artist as str
        @param cancellable as Gio.Cancellable
        @return uris as [str]
    """
    try:
        mbid = get_musicbrainz_mbid(artist)
        print("mbid = {}".format(mbid))
        if mbid is None:
            return ""
        url = "http://webservice.fanart.tv/v3/music/{}?api_key={}".format(mbid, FANART_API_KEY)
        
        print("api : {}".format(url))
        
        response = requests.get(url)
        if response.status_code == 200:
            json_data = response.json()
            
            # print(json.dumps(json_data, indent=2))
            
            key = ""
            if "musiclogo" in json_data:
                key = "musiclogo"
            elif "hdmusiclogo" in json_data:
                key = "hdmusiclogo"
            elif "artistthumb" in json_data:
                key = "artistthumb"
            elif "artistbackground" in json_data:
                key = "artistbackground"
            
            if key != "" :
                if len(json_data[key]) == 0: return ""
                return json_data[key][0]["url"]
                    
    except Exception as e:
        print("fanarttv exception : {}".format(e))
        print("url = {}".format(url))
    
    return ""

def get_deezer_artist_artwork_url(artist):
    """
        Get artist artwork using Deezer
        @param artist as str
        @return url as str
    """
    try:
        artist_formated = urllib.parse.quote_plus(artist).replace(" ", "+")
        url = "https://api.deezer.com/search/artist/?q={}&output=json&index=0".format(artist_formated)

        print("api : {}".format(url))

        response = requests.get(url)
        if response.status_code == 200:
            json_data = response.json()
            
            # print(json.dumps(json_data, indent=2))

            desired_artist = next((a for a in json_data["data"] if a["name"].lower() == artist.lower()), None)
            if desired_artist:
                return desired_artist["picture_medium"]
            
    except Exception as e:
        print("Deezer exception : {}".format(e))
        print("url = {}".format(url))
    return None

def get_artist_artwork(artist):
    url = get_fanarttv_artist_artwork_url(artist)
    if url == "":
        url = get_deezer_artist_artwork_url(artist)
    
    return url


def main():
    # Vérifier si des fichiers ont été spécifiés en arguments
    if len(sys.argv) < 2:
        print("Veuillez spécifier au moins un répertoire en argument.")
        return

    for directory in sys.argv[1:]:
        artist = os.path.basename(directory)
    
        print("searching for {} ....".format(artist))
        url = get_artist_artwork(artist)
        print("artwork = {}".format(url))
        print()
        
        if url != None:
            urllib.request.urlretrieve(str(url), os.path.join(directory, ".folder.jpg"))

            # On enregistre un fichier .directory (pour Dolphin)
            # Qui définit l'image téléchargée comme étant l'icône du répertoire artiste
            with open(os.path.join(directory, ".directory"), "w") as fichier:
                # Écrire du contenu dans le fichier
                fichier.write("[Desktop Entry]\n")
                fichier.write("Icon=./.folder.jpg")
        
        # time.sleep(1)

    print ("*** Finished ! ***")
    print ()
    print ("You can now close this window...")

if __name__ == "__main__":
    main()
