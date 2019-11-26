#!/bin/python3

from bs4 import BeautifulSoup
import requests

def extractor(track_name):
    main_url = "https://www.lyricfinder.org/search/tracks/"
    req_url = main_url + track_name
    header= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:67.0) Gecko/20100101 Firefox/67.0'}
    request = requests.get(req_url, headers=header).text
    soup = BeautifulSoup(request, "html.parser")

    songs = []
    links = []
    artists = []
    all_info = []

    for artist in soup.findAll('a', attrs={'class': 'artist-link'}):
        artist = artist.get_text().strip()
        artists.append(artist)

    for song in soup.findAll('a', attrs={'class': 'song-title-link'}):
        links.append(song['href'])
        song = song.get_text().strip()
        songs.append(song)

    for i in range(0, len(artists)):
        title = songs[i] + ' - ' + artists[i]
        info = {
            'title': title,
            'lyrics-link': links[i]
        }
        all_info.append(info)
    return all_info


track_name = input("Track name: ")
print(extractor(track_name))
