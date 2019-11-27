#!/bin/python3

import requests
from bs4 import BeautifulSoup
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters

def main():
    updater = Updater(token='Token'', use_context=True)
    dispatcher = updater.dispatcher

    def start(update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text="کافیه اسم آهنگی که متنش رو می‌خوای تایپ کنی!")

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)


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


    def get_track(update, context):
        def isEnglish(user_input):
            try:
                user_input.encode(encoding='utf-8').decode('ascii')
            except UnicodeDecodeError:
                return False
            else:
                return True

            
            if isEnglish(update.message.from_user) == True:
                context.bot.send_message(chat_id=update.effective_chat.id, text=print(extractor(update.message.from_user)))
            else:
                context.bot.send_message(chat_id=update.effective_chat.id, text='انگلیسی تایپ کن دیگه :)')

    track_handler = MessageHandler(Filters.text, get_track)
    dispatcher.add_handler(track_handler)

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
    
