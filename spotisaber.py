if input("\ndo you want to install spotipy and syncsaber api? (y/n): ") == "y":
    import os
    os.system('pip3 install spotipy')
    os.system('pip3 install beatsaver.py')
    os.system('pip3 install --upgrade pip')

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
from beatsaver.beatsaver import BeatSaver
import webbrowser
import time
print("**disclaimer the map that is downloaded is the map thats name most closely matches the search playlists songs name**")



#Authentication
client_credentials_manager = SpotifyClientCredentials(client_id="39bca5a1f9ee4f278b055725a1d8369d", client_secret="47ea9f911145410d8463e3b28d2d5052")
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
spotify_pl = []

#finding playlist


playlist_link = input("add your playlists share link here! : ")
while "https://open.spotify.com/playlist/" not in playlist_link:
    print("Not a valid link!")
    playlist_link = input("add a valid playlists share link here! : ")
    
playlist_URI = playlist_link.split("/")[-1].split("?")[0]
track_uris = [x["track"]["uri"] for x in sp.playlist_tracks(playlist_URI)["items"]]

#adding tracks to playlist
for track in sp.playlist_tracks(playlist_URI)["items"]:
    #URI
    track_uri = track["track"]["uri"]
    
    #Track name
    track_name = track["track"]["name"]
    
    spotify_pl.append(track_name)

#exporting as jason
"""
json_string = json.dumps(spotify_pl)
print(json_string)

with open('json_tracks.json', 'w') as outfile:
    json.dump(json_string, outfile)
"""
beat_download_lst = []

def search_song(spotify_pl, f, beat_download_lst):
    # Uses the beatsaver api to request song names
    beatsong_final = []
    difficulty = []
    beatsaver = BeatSaver(user_agent="beatsaber x spotify v0.0.1")
    beatsong_list = beatsaver.get_search_text(query=spotify_pl[f])
    beat_download = ""
    if len(beatsong_list) <= 0:
        print("-------------------------------------------- \n")
        print("Song {} not found \n" .format(spotify_pl[f]))
        return
    #turns the weird format to a string
    search1 = str(beatsong_list[0])
    #turns the string to a list based on commas
    string_list = search1.split(",")
    #searches the list for downloadURL
    beat_name = str(string_list[1])
    for i in range(len(string_list)):
        if "downloadURL" in string_list[i]:
            beat_download = string_list[i]
    
    for i in range(len(string_list)):
        if "difficulty" in string_list[i]:
            difficulty.append(string_list[i])
    
    #prints the name and download url
    print("-------------------------------------------- ")
    print("\nSong {} found! " .format(spotify_pl[f]))
    print("\nname: " + beat_name[7:len(beat_name) - 1])
    beat_download_trim = beat_download[14:len(beat_download) - 1]
    print("\ndownload link: " + beat_download_trim)
    beat_download_lst.append(beat_download_trim)
    
    #if theres "difficulty" in the discription it prints the description but i am unable to find a fix at the mome
    print("\ndifficulties: ")
    for i in range (0, len(difficulty)):
        trimmed = (difficulty[i])
        print(trimmed[13:len(difficulty[i]) - 1])

        
    print("")
# my personal playlist -> https://open.spotify.com/playlist/6fnTjhDz0q1RKGhmsAOHQF?si=6f118c238abb425f
ammount = int(input("--------------------------------------------\nhow many songs from your playlist do you want to add: "))

if ammount > len(spotify_pl):
    ammount = len(spotify_pl)
print("adding {} songs" .format(ammount))
for f in range(ammount):
    search_song(spotify_pl, f, beat_download_lst)


print("-------------------------------------------- ")
if input("download all tracks?(y/n): ") == "y":
    for i in range (0, ammount - 1):
        webbrowser.open(beat_download_lst[i])    

print("Thankyou for using spotisaber!")
time.sleep(10)
