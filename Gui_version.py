import tkinter as tk
import os
while True:
    try:
        from tkinter import *
        from tkinter import ttk
        import spotipy
        from spotipy.oauth2 import SpotifyClientCredentials
        from beatsaver.beatsaver import BeatSaver
        import webbrowser
        from tkscrolledframe import ScrolledFrame
        break
    except:
        os.system('pip3 install spotipy')
        os.system('pip3 install beatsaver.py')
        os.system('pip3 install --upgrade pip')
        os.system('pip install tkScrolledFrame')
        os.system('pip install tkinter')
global check
check = False

root = Tk()
root.geometry("600x500")
root.resizable(False, False)
root.title("test page")

canvas = Canvas(root,height=155,width=750,highlightbackground="black")
canvas.configure(background='black')
canvas.pack()

root.configure(background='black')
global style
style = ttk.Style()
style.theme_use('clam')
style.configure("button.TButton", font=('cocogoose', 20), relief="flat" ,foreground="black", background="green yellow", border="black", bordercolor = "black")
style.configure("button2.TButton", font=('arial', 10), relief="flat" ,foreground="black", background="green yellow", border="black", bordercolor = "black")

style.configure("TEntry", relief="flat" ,foreground="black", background="green yellow")
style.configure('TFrame', background='black')



def button_comfirm():
    global check
    playlist_link = entry.get()
    
    if "https://open.spotify.com/playlist/" not in playlist_link:
        lable = tk.Label(root, text = "That is an invalid spotify playlist link.", font=('arial 8'), fg = "red", bg = "black")
        lable.place(x=10,y=390)
        return

    if check == True:
        pass
    else:
        lable = tk.Label(root, text = "disclaimer Maps may be inacurate due to simmilar song names!", font=('arial 8'), fg = "green", bg = "black")
        lable.place(x=140,y=400)
        check = True
        return
    
    
    
    print("work")
    

    
    for widgets in root.winfo_children():
          if str(widgets) != ".!canvas":
                widgets.destroy()
    lable_title = tk.Label(canvas, text = "Song selection.", font=('biko 50 bold'),bg = "green yellow", fg = "black")
    lable_title.place(x=10,y=1)
       


    # Authentication (authenticates to the spotify api)
    client_credentials_manager = SpotifyClientCredentials(client_id="39bca5a1f9ee4f278b055725a1d8369d", client_secret="3cc1d92c25184b3c85f40fb15c417742")
    sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
    spotify_pl = []

    # my personal playlist -> https://open.spotify.com/playlist/6fnTjhDz0q1RKGhmsAOHQF?si=6f118c238abb425f (for testing)

    # requests With the ID
    playlist_URI = playlist_link.split("/")[-1].split("?")[0]
    track_uris = [x["track"]["uri"] for x in sp.playlist_tracks(playlist_URI)["items"]]

    #adding tracks to playlist
    for track in sp.playlist_tracks(playlist_URI)["items"]:
        # request track uri
        track_uri = track["track"]["uri"]
        
        # request Track name
        track_name = track["track"]["name"]

        # adding trackname to list
        spotify_pl.append(track_name)

    # exporting playlist as jason
    # beatdownload defined
    beat_download_lst = []
    global song_list

    frame_top = tk.Frame(root, width=400, height=250)
    frame_top.pack(side="top", expand=1, fill="both")

    # Create a ScrolledFrame widget
    sf = ScrolledFrame(frame_top, width=380, height=240)
    sf.pack(side="top", expand=1, fill="both")

    # Bind the arrow keys and scroll wheel
    sf.bind_arrow_keys(frame_top)
    sf.bind_scroll_wheel(frame_top)

    frame = sf.display_widget(tk.Frame)

    def callback(url):
       webbrowser.open_new_tab(url)



    def search_song(spotify_pl, f, beat_download_lst):
        global song_list
        song_list = ""
        # Uses the beatsaver api to request song names
        difficulty = []
        beatsaver = BeatSaver(user_agent="beatsaber x spotify v0.0.1")
        beatsong_list = beatsaver.get_search_text(query=spotify_pl[f])
        beat_download = ""
        if len(beatsong_list) <= 0:
            song_list += ("Song {} not found \n" .format(spotify_pl[f]))
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
        # searching for difficulty's
        for i in range(len(string_list)):
            if "difficulty" in string_list[i]:
                difficulty.append(string_list[i])
        
        # printing the name, download url and difficulties
        song_list += ("\nSong {} found! " .format(spotify_pl[f]))
        song_list += ("\nname: " + beat_name[7:len(beat_name) - 1])
        beat_download_trim = beat_download[14:len(beat_download) - 1]
        song_list += ("\ndownload link: " + beat_download_trim)
        beat_download_lst.append(beat_download_trim)

        # if theres "difficulty" in the discription it prints the description but i am unable to find a fix at the mome
        song_list += ("\ndifficulties: ")
        for i in range (0, len(difficulty)):
            trimmed = (difficulty[i])
            song_list += (trimmed[13:len(difficulty[i]) - 1])

        
        song_list += ("")
        link = tk.Label(frame, text = str(song_list), cursor="hand2")
        if song_list.strip == "": 
            link = tk.Label(frame, text = "song {} not found" .format(spotify_pl[f]))
        link.bind("<Button-1>", lambda e:
        callback(str(beat_download_trim)))
        link.pack(side = TOP, pady=20, padx = 7)
        print(beat_download_trim)
        

    # asking for the ammount of songs to be downloaded (sets to length of plalist if a number higher than the playlist is given)
    

    # running the seaching and printing for songs
    for f in range(len(spotify_pl)):
        search_song(spotify_pl, f, beat_download_lst)
    print(beat_download_lst)
    def down_all():
            for i in range (0, len(spotify_pl) - 1):
                webbrowser.open(beat_download_lst[i])
    
    # downloading maps found
    ttk.Button(frame, text = "download all tracks?", command=down_all).place(x=0,y=0) #side = TOP, pady=20, padx = 7
      


def libraries_download():
    import os
    os.system('pip3 install spotipy')
    os.system('pip3 install beatsaver.py')
    os.system('pip3 install --upgrade pip')
    os.system('pip install tkScrolledFrame')
lable_title = tk.Label(canvas, text = "Add playlist.", font=('biko 50 bold'),bg = "green yellow", fg = "black")
lable_title.place(x=10,y=1)

lable = tk.Label(root, text = "Playlist link:", font=('arial 25'),  fg = "yellow green", bg = "black")
lable.place(x=7,y=120)
canvas.create_rectangle(0, 0, 1000, 100, outline="black", fill="green yellow")
button = ttk.Button(root, text = "Confirm", command=button_comfirm, style = "button.TButton")
button.pack(side = BOTTOM, pady=20)
button = ttk.Button(root, text = "Download Libraries", command=libraries_download, style = "button2.TButton")
button.place(x= 6, y = 220)
entry = tk.Entry(root, text = "", font=('arial 15'), fg = "gray", width= 20, bg = "yellow green")
entry.place(x=7,y=170)



if __name__ == '__main__':
        root.mainloop()



