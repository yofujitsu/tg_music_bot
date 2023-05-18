import setuptools
import random
import telebot
from telebot import types
from aiogram.types import *
# import vk_api
import aiogram
import requests
from bs4 import BeautifulSoup as b
from yandex_music import Client
from yandex_parser import MyPerson

client = Client('AQAAAAASg-EiAAG8Xth12jSrvkhtqzxHtyTafzo').init()
track = client.users_likes_tracks()[4]
API_TOKEN = "5952876513:AAEG1jg7AiXYmPPx9U5_FraCq00HYEztkwE"

bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=['start'])
def hello(message):
    bot.send_message(message.chat.id,
                     text="""Привет! Если хочешь ознакомиться с командами - жми menu. Хочешь узнать, что делает каждая команда - жми help. Отправь мне стикер)""")
    markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("menu")
    btn2 = types.KeyboardButton("help")
    markup1.add(btn1, btn2)
    bot.send_message(message.chat.id, text="ну че", reply_markup=markup1)


@bot.message_handler(commands=['my', 'rs', 's', 'ps', 'help'])
def commands_rofl(message):
    bot.send_message(message.chat.id, "пока не готово :(")


@bot.message_handler(commands=['menu'])
def send_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Что я могу?")
    btn2 = types.KeyboardButton("Музыка из профиля")
    btn3 = types.KeyboardButton("Музыка из плейлиста")
    btn4 = types.KeyboardButton("Музыка из чартов")
    btn5 = types.KeyboardButton("Музыка из рекомендаций")
    btn6 = types.KeyboardButton("Общий поиск из базы")
    back = types.KeyboardButton("Вернуться в главное меню")
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6, back)
    bot.send_message(message.chat.id, text="ну че", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def bebra(message):
    if (message.text == "menu"):
        send_menu(message)

    elif (message.text == "help"):
        bot.send_message(message.chat.id, text="не могу помочь с этим.")

    elif ((message.text == "Что я могу?") or (message.text == "Музыка из плейлиста") or (
            message.text == "Музыка из чартов") or
          (message.text == "Музыка из рекомендаций") or (message.text == "Общий поиск из базы")):
        bot.send_message(message.chat.id, text="пока не готово. соре.")

    elif (message.text == "Музыка из профиля"):
        client.users_likes_tracks()[5].fetch_track().download(
            f"{', '.join(client.tracks(track.id)[0].artists_name()), '-', client.tracks(track.id)[0].title}.mp3")
        audio = open(
            f"{', '.join(client.tracks(track.id)[0].artists_name()), '-', client.tracks(track.id)[0].title}.mp3", 'rb')
        bot.send_audio(message.chat.id, audio)
        bot.send_message(message.chat.id, text=")")
        audio.close()

    elif (message.text == "Вернуться в главное меню"):
        bot.send_message(message.chat.id, text="waltuh... -_-", reply_markup=None)
        hello(message)
    else:
        bot.send_photo(message.chat.id,
                       photo='https://forum.valhalla-age.org/uploads/monthly_2020_04/CnCCKw3XYAEYEU_.jpg.336b77f8c4a034683c214c220f9e7073.jpg')


me = MyPerson('AQAAAAASg-EiAAG8Xth12jSrvkhtqzxHtyTafzo')
me.page += 2
print(me.page)
print(me.get_likes_tracks()[0].title)


@bot.message_handler(content_types=['sticker'])
def cmd_inline_url(message: types.Message):
    tracks_titles = me.get_likes_tracks()
    buttons = [
        # types.InlineKeyboardButton(text=track.titles[0], callback_data="track_1"),
        # types.InlineKeyboardButton(text="track 2", callback_data="track_2"),
        # types.InlineKeyboardButton(text="track 3", callback_data="track_3"),
        # types.InlineKeyboardButton(text="track 4", callback_data="track_4"),
        # types.InlineKeyboardButton(text="track 5", callback_data="track_5")
    ]
    for i in range(len(tracks_titles)):
        buttons.append(types.InlineKeyboardButton(text=tracks_titles[i].author + " " + tracks_titles[i].title,
                                               callback_data='i'+tracks_titles[i].id))
    keyboard = types.InlineKeyboardMarkup(row_width=1).add(*buttons)
    low_row = [
        types.InlineKeyboardButton(text="1", callback_data="curr_page"),
        types.InlineKeyboardButton(text="<-", callback_data="prev"),
        types.InlineKeyboardButton(text="curr page", callback_data="curr"),
        types.InlineKeyboardButton(text="->", callback_data="next"),
        types.InlineKeyboardButton(text="last page", callback_data="last_page")
    ]
    low_links = [
        types.InlineKeyboardButton(text="creator 1", url="https://github.com/yofujitsu"),
        types.InlineKeyboardButton(text="creator 2", url="https://github.com/Ulquiorrashif"),
    ]
    keyboard.row(*low_row)
    keyboard.row(*low_links)

    bot.send_message(message.chat.id, text="Список аудиозаписей", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def my_favourites(call):
    if call.data[0] == 'i':
        print(call.data[1:])
        print(me.mytrack[1].id)
        audio_title = me.download(call.data[1:])
        print(audio_title)
        audio = open(audio_title, "rb")
        bot.send_message(call.message.chat.id, call.data)
        bot.send_audio(call.message.chat.id, audio)
    if call.data == "next":
        me.page+=1
        tracks_titles = me.get_likes_tracks()
        buttons = [
            # types.InlineKeyboardButton(text=track.titles[0], callback_data="track_1"),
            # types.InlineKeyboardButton(text="track 2", callback_data="track_2"),
            # types.InlineKeyboardButton(text="track 3", callback_data="track_3"),
            # types.InlineKeyboardButton(text="track 4", callback_data="track_4"),
            # types.InlineKeyboardButton(text="track 5", callback_data="track_5")
        ]
        for i in range(len(tracks_titles)):
            buttons.append(types.InlineKeyboardButton(text=tracks_titles[i].author + " " + tracks_titles[i].title,
                                                      callback_data='i' + tracks_titles[i].id))
        keyboard = types.InlineKeyboardMarkup(row_width=1).add(*buttons)
        low_row = [
            types.InlineKeyboardButton(text="1", callback_data="curr_page"),
            types.InlineKeyboardButton(text="<-", callback_data="prev"),
            types.InlineKeyboardButton(text="curr page", callback_data="curr"),
            types.InlineKeyboardButton(text="->", callback_data="next"),
            types.InlineKeyboardButton(text="last page", callback_data="last_page")
        ]
        low_links = [
            types.InlineKeyboardButton(text="creator 1", url="https://github.com/yofujitsu"),
            types.InlineKeyboardButton(text="creator 2", url="https://github.com/Ulquiorrashif"),
        ]
        keyboard.row(*low_row)
        keyboard.row(*low_links)
        bot.send_message(call.message.chat.id, text="Список аудиозаписей", reply_markup=keyboard)


bot.polling()
