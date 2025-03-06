import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from pprint import pprint

load_dotenv()

"""
Music Time Machine - Spotifyプレイリスト作成プログラム

📌 プログラム概要 / Program Overview:
このプログラムは、指定された日付のBillboard Hot 100のトップソングを取得し、Spotifyのプレイリストとして作成する。
This program fetches the top songs from the Billboard Hot 100 for a given date and creates a playlist in Spotify.

📌 使用する機能 / Features:
1. Billboardから指定された日付のトップ100ソングを取得 / Fetch top 100 songs from Billboard for the given date.
2. 各曲のSpotifyのURIを検索し、プレイリストを作成 / Search for each song's Spotify URI and create a playlist.
3. 作成したプレイリストにトップ100の曲を追加 / Add the top 100 songs to the created playlist in Spotify.

📌 参照しているAPI / APIs Used:
- Billboard API: https://www.billboard.com/charts/hot-100/
- Spotify API: https://developer.spotify.com/documentation/web-api/

📌 環境変数 (.env) / Environment Variables:
- SPOTIFY_CLIENT_ID=your_spotify_client_id
- SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
- SPOTIFY_DISPLAY_NAME=your_spotify_display_name

"""

# Billboardからデータを取得する / Scraping Billboard data
date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")

url = "https://www.billboard.com/charts/hot-100/" + date
header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0"}

response = requests.get(url=url, headers=header)
website = response.text
soup = BeautifulSoup(website, "html.parser")

all_songs = soup.select("li ul li h3")
song_titles = [song.getText().strip() for song in all_songs]
# print(song_titles)

# Spotifyの認証情報を設定する / Setting up Spotify authentication
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_DISPLAY_NAME = os.getenv("SPOTIFY_DISPLAY_NAME")

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri="http://example.com",
        scope="playlist-modify-private",
        show_dialog=True,
        cache_path="token.txt",
        username=SPOTIFY_DISPLAY_NAME,
    )
)

user_id = sp.current_user()["id"]

# 曲のURIを取得する / Retrieving song URIs
year = date.split("-")[0]
song_uris = []

for song in song_titles:
    query = f"track: {song} year: {year}"
    result = sp.search(query, type="track")
    # pprint(result)

    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

# print(song_uris)

# プレイリストを作成する / Creating a playlist
create_playlist = sp.user_playlist_create(
    user=user_id,
    name=f"{date} Billboard 100",
    public=False,
    collaborative=False,
    description="",
)

# プレイリストに曲を追加する / Adding songs to the playlist
sp.playlist_add_items(playlist_id=create_playlist["id"], items=song_uris)
