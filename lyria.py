#!/bin/python3

import logging
import requests
from bs4 import BeautifulSoup
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


# Logging 
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Start button command
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="کافیه اسم آهنگی که متنش رو می‌خوای تایپ کنی!")


# Scrapes the data out of web.
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

        ## This is a fucking test
        
        context.bot.send_message(chat_id=update.effective_chat.id, text='صبر کن دارم پیدا می‌کنم \n %s' % (all_info))
        

# Checks if the track's name is written in English
def isEnglish(user_input):
    try:
        user_input.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True

# If text is in English it passes the text to extractor
def get_track(update, context):
    if isEnglish(update.message.text):
        extractor(update.message.text, update, context)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='انگلیسی تایپ کن دیگه :)')


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    ####  Starting the bot ####

    # creates Updater and passes TOKEN
    updater = Updater(token='1006025104:AAEltikc297DUmXylZ51z3_TFFvSWaeZ1ko', use_context=True)
    
    # Getting dispatcher to register handlers
    dp = updater.dispatcher

    # Registering my functions
    start_handler = CommandHandler('start', start)
    track_handler = MessageHandler(Filters.text, get_track)
    #extractor_handler = MessageHandler(Filters.text, extractor)

    #dp.add_handler(extractor_handler)
    dp.add_handler(track_handler)
    dp.add_handler(start_handler)

    # Registering Error fuctions
    dp.add_error_handler(error)
    
    # Starts BOT
    updater.start_polling()

    # Keep it active untile CTRL + C
    updater.idle()

if __name__ == "__main__":
    main()
    
