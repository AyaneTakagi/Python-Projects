import requests
from bs4 import BeautifulSoup

# 📌 プログラム概要 / Program Overview:
# このプログラムは、Empire Onlineの映画ランキングページから映画タイトルを取り出し、
# BeautifulSoupを使ってHTMLを解析して、映画タイトルを逆順に並べた後、それらをテキストファイルに保存する。
# This program fetches movie titles from the Empire Online movie ranking page, parses the HTML using BeautifulSoup,
# reverses the movie titles' order, then saves them into a text file.

URL = "https://web.archive.org/web/20200518073855/https://www.empireonline.com/movies/features/best-movies-2/"

response = requests.get(url=URL)
website = response.text

soup = BeautifulSoup(website, "html.parser")

all_movies = soup.find_all(name="h3", class_="title")

movie_titles = [movie.getText() for movie in all_movies]
movies = movie_titles[::-1]

with open("movies.txt", mode="w") as file:
    for movie in movies:
        file.write(f"{movie}\n")