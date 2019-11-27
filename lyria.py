#!/bin/python3

import requests
from bs4 import BeautifulSoup
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup



def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="کافیه اسم آهنگی که متنش رو می‌خوای تایپ کنی!")

    


def extractor(track_name, update, context):
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
    
    
    button_list = []
    for i in range(0, len(artists)):
        button_list.append('InlineKeyboardButton(%s, callback_data=%s)' % (all_info[i]['title'], all_info[i]['lyrics_link']))
        reply_markup = InlineKeyboardMarkup(util.build_menu(button_list, n_cols=2))
        context.bot.send_message(chat_id=update.effective_chat.id, text='نتایج:', reply_markup=reply_markup)



def isEnglish(user_input):
    try:
        user_input.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True

def get_track(update, context):
    if isEnglish(update.message.text):
        extractor(update.message.text, update, context)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='انگلیسی تایپ کن دیگه :)')




def main():
    updater = Updater(token='TOKEN', use_context=True)
    dispatcher = updater.dispatcher
    start_handler = CommandHandler('start', start)
    track_handler = MessageHandler(Filters.text, get_track)
    dispatcher.add_handler(track_handler)
    dispatcher.add_handler(start_handler)
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
    
