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
    btn2 = types.KeyboardButton("Мне нравится")
    btn3 = types.KeyboardButton("Музыка из плейлиста")
    btn4 = types.KeyboardButton("Музыка из чартов")
    btn5 = types.KeyboardButton("Музыка из рекомендаций")
    btn6 = types.KeyboardButton("Поиск")
    back = types.KeyboardButton("Вернуться в главное меню")
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6, back)
    bot.send_message(message.chat.id, text="ну че", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def bebra(message):
    if (message.text == "menu"):
        send_menu(message)

    elif (message.text == "help"):
        bot.send_message(message.chat.id, text="не могу помочь с этим.")

    elif ((message.text == "Что я могу?") or (
            message.text == "Музыка из чартов") or
          (message.text == "Музыка из рекомендаций")):
        bot.send_message(message.chat.id, text="пока не готово. соре.")

    elif (message.text == "Мне нравится"):
        cmd_inline_url(message)

    elif message.text == 'Музыка из плейлиста':
        my_playlists(message)

    elif message.text == "Поиск":
        msg = bot.send_message(message.chat.id, "Напишите, что хотите найти:")
        bot.register_next_step_handler(msg, search2)

    elif (message.text == "Вернуться в главное меню"):
        bot.send_message(message.chat.id, text="waltuh... -_-", reply_markup=None)
        hello(message)
    else:
        bot.send_photo(message.chat.id,
                       photo='https://forum.valhalla-age.org/uploads/monthly_2020_04/CnCCKw3XYAEYEU_.jpg.336b77f8c4a034683c214c220f9e7073.jpg')


me = MyPerson('AQAAAAASg-EiAAG8Xth12jSrvkhtqzxHtyTafzo')
def search2(message):
    q = me.search(message.text)
    bot.send_message(message.chat.id, q)

@bot.message_handler(commands=['my'])
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
                                               callback_data='i'+str(tracks_titles[i].id)))
    keyboard = types.InlineKeyboardMarkup(row_width=1).add(*buttons)
    low_row = [
        types.InlineKeyboardButton(text="<-", callback_data="prev_my"),
        types.InlineKeyboardButton(text="1", callback_data="curr_page_my"),
        types.InlineKeyboardButton(text="->", callback_data="next_my")
    ]
    low_links = [
        types.InlineKeyboardButton(text="creator 1", url="https://github.com/yofujitsu"),
        types.InlineKeyboardButton(text="creator 2", url="https://github.com/Ulquiorrashif"),
    ]
    keyboard.row(*low_row)
    keyboard.row(*low_links)

    bot.send_message(message.chat.id, text="Список аудиозаписей", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def buttons_query_handler(call: CallbackQuery):
    if call.data[0] == 'i':
        print(type(call.data))
        audio_title = me.download(str(call.data[1:]))
        audio = open(audio_title, "rb")
        # bot.send_message(call.message.chat.id, call.data)
        bot.send_audio(call.message.chat.id, audio)
    if call.data[0] == "P":
        me.setPlaylist(call.data[1:])
        print(call.data[1:])
        tracks = me.get_tracks_by_playlist()
        buttons = []
        for i in range(len(tracks)):
            buttons.append(types.InlineKeyboardButton(text=tracks[i].author + " " + tracks[i].title,
                                                      callback_data='i' + str(tracks[i].id)))
        keyboard = types.InlineKeyboardMarkup(row_width=1).add(*buttons)
        low_row = [
            types.InlineKeyboardButton(text="<-", callback_data="prev_pl_tr"),
            types.InlineKeyboardButton(text=me.page, callback_data="curr_page_pl_tr"),
            types.InlineKeyboardButton(text="->", callback_data="next_pl_tr")
        ]
        low_links = [
            types.InlineKeyboardButton(text="creator 1", url="https://github.com/yofujitsu"),
            types.InlineKeyboardButton(text="creator 2", url="https://github.com/Ulquiorrashif"),
        ]
        keyboard.row(*low_row)
        keyboard.row(*low_links)

        bot.send_message(call.message.chat.id, text="Список треков в плейлисте", reply_markup=keyboard)
    if call.data == "next_my":
        # me.page+=1
        tracks_titles = me.get_likes_tracks(1)
        buttons = []
        for i in range(len(tracks_titles)):
            buttons.append(types.InlineKeyboardButton(text=tracks_titles[i].author + " " + tracks_titles[i].title,
                                                      callback_data='i' + str(tracks_titles[i].id)))
        keyboard = types.InlineKeyboardMarkup(row_width=1).add(*buttons)
        low_row = [
            types.InlineKeyboardButton(text="<-", callback_data="prev_my"),
            types.InlineKeyboardButton(text=me.page, callback_data="curr_page_my"),
            types.InlineKeyboardButton(text="->", callback_data="next_my")
        ]
        low_links = [
            types.InlineKeyboardButton(text="creator 1", url="https://github.com/yofujitsu"),
            types.InlineKeyboardButton(text="creator 2", url="https://github.com/Ulquiorrashif"),
        ]
        keyboard.row(*low_row)
        keyboard.row(*low_links)
        bot.send_message(call.message.chat.id, text="Список аудиозаписей", reply_markup=keyboard)
    if call.data == "prev_my" and me.page>1:
        # me.page-=1
        tracks_titles = me.get_likes_tracks(-1)
        buttons = []
        for i in range(len(tracks_titles)):
            buttons.append(types.InlineKeyboardButton(text=tracks_titles[i].author + " " + tracks_titles[i].title,
                                                      callback_data='i' + str(tracks_titles[i].id)))
        keyboard = types.InlineKeyboardMarkup(row_width=1).add(*buttons)
        low_row = [
            types.InlineKeyboardButton(text="<-", callback_data="prev_my"),
            types.InlineKeyboardButton(text=me.page, callback_data="curr_page_my"),
            types.InlineKeyboardButton(text="->", callback_data="next_my")
        ]
        low_links = [
            types.InlineKeyboardButton(text="creator 1", url="https://github.com/yofujitsu"),
            types.InlineKeyboardButton(text="creator 2", url="https://github.com/Ulquiorrashif"),
        ]
        keyboard.row(*low_row)
        keyboard.row(*low_links)
        bot.send_message(call.message.chat.id, text="Список аудиозаписей", reply_markup=keyboard)
    if call.data == "next_pl_tr":
        # me.page+=1
        tracks_titles = me.get_tracks_by_playlist(1)
        buttons = []
        for i in range(len(tracks_titles)):
            buttons.append(types.InlineKeyboardButton(text=tracks_titles[i].author + " " + tracks_titles[i].title,
                                                      callback_data='i' + str(tracks_titles[i].id)))
        keyboard = types.InlineKeyboardMarkup(row_width=1).add(*buttons)
        low_row = [
            types.InlineKeyboardButton(text="<-", callback_data="prev_pl_tr"),
            types.InlineKeyboardButton(text=me.page, callback_data="curr_page_pl_tr"),
            types.InlineKeyboardButton(text="->", callback_data="next_pl_tr")
        ]
        low_links = [
            types.InlineKeyboardButton(text="creator 1", url="https://github.com/yofujitsu"),
            types.InlineKeyboardButton(text="creator 2", url="https://github.com/Ulquiorrashif"),
        ]
        keyboard.row(*low_row)
        keyboard.row(*low_links)
        bot.send_message(call.message.chat.id, text="Список аудиозаписей из плейлиста", reply_markup=keyboard)
    if call.data == "prev_pl_tr" and me.page>1:
        # me.page-=1
        print("<-")
        tracks_titles = me.get_tracks_by_playlist(-1)
        buttons = []
        for i in range(len(tracks_titles)):
            buttons.append(types.InlineKeyboardButton(text=tracks_titles[i].author + " " + tracks_titles[i].title,
                                                      callback_data='i' + str(tracks_titles[i].id)))
        keyboard = types.InlineKeyboardMarkup(row_width=1).add(*buttons)
        low_row = [
            types.InlineKeyboardButton(text="<-", callback_data="prev_pl_tr"),
            types.InlineKeyboardButton(text=me.page, callback_data="curr_page_pl_tr"),
            types.InlineKeyboardButton(text="->", callback_data="next_pl_tr")
        ]
        low_links = [
            types.InlineKeyboardButton(text="creator 1", url="https://github.com/yofujitsu"),
            types.InlineKeyboardButton(text="creator 2", url="https://github.com/Ulquiorrashif"),
        ]
        keyboard.row(*low_row)
        keyboard.row(*low_links)
        bot.send_message(call.message.chat.id, text="Список аудиозаписей из плейлиста", reply_markup=keyboard)

@bot.message_handler(commands=['ps'])
def my_playlists(message):
    pl = me.get_playlists()
    buttons = [
        # types.InlineKeyboardButton(text=track.titles[0], callback_data="track_1"),
        # types.InlineKeyboardButton(text="track 2", callback_data="track_2"),
        # types.InlineKeyboardButton(text="track 3", callback_data="track_3"),
        # types.InlineKeyboardButton(text="track 4", callback_data="track_4"),
        # types.InlineKeyboardButton(text="track 5", callback_data="track_5")
    ]
    for i in range(len(pl)):
        buttons.append(types.InlineKeyboardButton(text=pl[i][0],
                                                  callback_data='P' + pl[i][1]))
    keyboard = types.InlineKeyboardMarkup(row_width=1).add(*buttons)
    low_row = [
        types.InlineKeyboardButton(text="<-", callback_data="prev_pl"),
        types.InlineKeyboardButton(text=me.page, callback_data="curr_page_pl"),
        types.InlineKeyboardButton(text="->", callback_data="next_pl")
    ]
    low_links = [
        types.InlineKeyboardButton(text="creator 1", url="https://github.com/yofujitsu"),
        types.InlineKeyboardButton(text="creator 2", url="https://github.com/Ulquiorrashif"),
    ]
    keyboard.row(*low_row)
    keyboard.row(*low_links)

    bot.send_message(message.chat.id, text="Список плейлистов", reply_markup=keyboard)

bot.polling()
