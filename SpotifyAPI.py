import requests
import base64
import json
from dotenv import dotenv_values
import tkinter as tk
from tkinter import ttk


# Constants
SECRETS = dotenv_values(".env")
REQUEST_CLIENT_URL = "https://accounts.spotify.com/api/token"
SEARCH_ENDPOINT_URL = "https://api.spotify.com/v1/search"
SPOTIFY_TOKEN = None

def get_token():
    # Prepare headers information
    auth_string = SECRETS["CLIENT_ID"] + ":" + SECRETS["CLIENT_SECRET"]
    auth_bytes = auth_string.encode("utf-8")
    auth_bytes = base64.b64encode(auth_bytes)
    encoded_string = auth_bytes.decode("utf-8")

    headers = {"Authorization" : "Basic " + encoded_string,
               "Content-Type" : "application/x-www-form-urlencoded"}
    
    body = {"grant_type" : "client_credentials"}

    response = requests.post(REQUEST_CLIENT_URL, headers = headers, data = body)
    json_response = json.loads(response.content)

    return json_response["access_token"]

# <------------ NEW FUNCTION ------------> #

def print_artist_info(artist):
    print()
    print("Artist's name: " + artist["name"])
    print("Artist's popularity: " + str(artist["popularity"]))
    print("Artist's genres: " + str(artist["genres"]))
    print("Artist's followers: " + str(artist["followers"]["total"]))
    print("Artist's Spotify ID: " + artist["id"])
    print("Spotify page: " + artist["external_urls"]["spotify"])
    print()

# <------------ NEW FUNCTION ------------> #

def get_artist_image(artist):
    artist_image = None

    for i in range(len(artist["images"])):
        if (i == 0):
            artist_image = artist["images"][0]
        elif (artist_image["height"] * artist_image["width"] < 
                artist["images"][i]["height"] * artist["images"][i]["width"]):
            artist_image = artist["images"][i]
    
    return artist_image

# <------------ NEW FUNCTION ------------> #

def get_wanted_artist(artists, artist_name):

    for artist in artists:
        if artist["name"] == artist_name:
            return artist
    
    print("<----- TO BE IMPLEMENTED ----->")
    print("WAS NOT ABLE TO FIND YOU ARTIST AUTOMATICALLY, PLEASE SELEECT THEM MANUALLY!")
    print("<----- TO BE IMPLEMENTED ----->")

# <------------ NEW FUNCTION ------------> #

def get_entry(entryString):
    artist_name = entryString.strip()
    artist_name_query = artist_name.replace(" ", "+")

    # Construct quering URL and header
    search_url = SEARCH_ENDPOINT_URL + "?q=" + artist_name_query + "&type=artist"
    header = {"Authorization" : "Bearer " + SPOTIFY_TOKEN}

    # Get server response and print it
    response = requests.get(search_url, headers = header)
    artists = json.loads(response.content)["artists"]["items"]

    artist = get_wanted_artist(artists, artist_name)
    print_artist_info(artist)
    image = get_artist_image(artist)
    print(image)


# <------------ NEW FUNCTION ------------> #

def main():

    # Get token
    global SPOTIFY_TOKEN
    SPOTIFY_TOKEN = get_token()

    # Setting up the window
    window = tk.Tk()
    window.title("Spotify API app")
    window.geometry("600x400")
    window.iconbitmap("C:\\Users\\kikib\\Desktop\\spotifyAPI\\spotify.ico")

    # Widgets
    label1 = ttk.Label(window, text = "Enter artist's name: ")
    label1.pack(pady = 10)

    entryString = tk.StringVar()
    entry = ttk.Entry(window, textvariable = entryString)
    entry.pack(pady = 10)

    button = ttk.Button(window, text = "Search!", command = lambda : get_entry(entryString.get()))
    button.pack(pady = 10)

    # Running the window
    window.mainloop()   


if __name__ == "__main__":
    main()