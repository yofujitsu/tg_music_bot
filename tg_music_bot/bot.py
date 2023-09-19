import asyncio

import setuptools
import random
import telebot
from aiogram import *
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from telebot import types
from aiogram.types import *
import aiogram
import requests
from bs4 import BeautifulSoup as b
from yandex_music import Client, Client
from yandex_music.exceptions import UnauthorizedError
import logging

from yandex_parser import MyAsyncPerson, MyPerson

logging.basicConfig(level=logging.INFO, filename='app.log',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.Logger

# 'y0_AgAAAAA-m1eKAAG8XgAAAADjdu60-k8-pH7FQ2u9v4GHmaRAFx_JP60'
# 'AQAAAAASg-EiAAG8Xth12jSrvkhtqzxHtyTafzo'
API_TOKEN = "5952876513:AAEG1jg7AiXYmPPx9U5_FraCq00HYEztkwE"
API_TOKEN2 = "6332135762:AAGCd8YOJNsYQmCemRG0upvt7Fq2vO7ZIq4"
lastId = 0

bot = telebot.TeleBot(API_TOKEN2)

# bot2 = Bot(token=API_TOKEN)
# storage = MemoryStorage()
# dp = Dispatcher(bot2, storage=storage)

me = MyPerson()
# me = MyAsyncPerson()
# Делаем базу данных
# class Mydb():
#     def __init__(self):
#         self.Db = {}
#     def swap(self,id):
#         try:
#             self.Db[id]
Db = {}


@bot.message_handler(commands=['start'])
def hello(message):
    markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("menu")
    btn2 = types.KeyboardButton("help")
    markup1.add(btn1, btn2)
    bot.send_message(message.chat.id,
                     text="""Привет! Если хочешь ознакомиться с командами - жми menu. Хочешь узнать, что делает каждая команда - жми help.""",
                     reply_markup=markup1)

#ЗДЕСЬ ОШИБКА
@bot.message_handler(commands=['help1'])
def commands_rofl(message):
    bot.send_message(message.chat.id,
                     text="Привет! Я телеграм-бот, который поможет тебе скачать твою музыку из стриминговой платформы Яндекс.Музыка. С моей помощью ты сможешь:"
                          "получать музыку из плейлиста 'Мне нравится', а также добавлять туда треки из других источников; получать музыку из добавленных альбомов и собственных плейлистов. "
                          "Для доступа к этим данным тебе необходимо авторизоваться. Список команд доступен по кнопке слева в чате. Сила в музыке! ")


@bot.message_handler(commands=['menu'])
def send_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Что я могу?")
    btn2 = types.KeyboardButton("Мне нравится")
    btn3 = types.KeyboardButton("Музыка из моих плейлистов")
    btn4 = types.KeyboardButton("Музыка из моих альбомов")
    btn5 = types.KeyboardButton("Войти")
    btn6 = types.KeyboardButton("Выйти")
    btn7 = types.KeyboardButton("Поиск")
    back = types.KeyboardButton("Вернуться в главное меню")
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, back)
    bot.send_message(message.chat.id, text="меню", reply_markup=markup)


@bot.message_handler(commands=['auth'])
def auth(message):
    # if me.getTOKEN() == '':
    #     msg = bot.send_message(message.chat.id,
    #                            "Для входа в аккаунт вам необходимо ввести Токен. Шпаргалка по получению токена доступна по ссылке ниже. Вы должны прислать строку без кавычек! Не бойтесь, мы не крадем ваши персональные данные, токен используется лишь для доступа к музыкальному каталогу пользователя.")
    #     bot.send_message(message.chat.id, "https://yandex-music.readthedocs.io/en/main/token.html")
    #     bot.register_next_step_handler(msg, auth2)
    # else:
    #     bot.send_message(message.chat.id, "Вы уже вошли с свой аккаунт!")
    try:
        me.setTOKEN(Db[message.chat.id])
        bot.send_message(message.chat.id, "Вы уже вошли с свой аккаунт!")
    except KeyError:
        msg = bot.send_message(message.chat.id,
                               "Для входа в аккаунт вам необходимо ввести Токен. Шпаргалка по получению токена доступна по ссылке ниже. Вы должны прислать строку без кавычек! Не бойтесь, мы не крадем ваши персональные данные, токен используется лишь для доступа к музыкальному каталогу пользователя.")
        bot.send_message(message.chat.id, "https://yandex-music.readthedocs.io/en/main/token.html")
        bot.register_next_step_handler(msg, auth2)


def auth2(message):
    try:
        me.setTOKEN(message.text)  # client = Client(message.text).init()
        Db[message.chat.id] = message.text
        bot.send_message(message.chat.id, "Вы успешно вошли в аккаунт!")
        send_menu(message)
    except UnauthorizedError or UnicodeEncodeError:
        me.setTOKEN('')
        # client = Client().init()
        bot.send_message(message.chat.id,
                         "Вы ввели невалидный токен. Внимательно прочитайте мануал. Пишите /auth для повторной попытки.")


@bot.message_handler(commands=['exit'])
def unauth(message):
    # if me.getTOKEN() == '':
    #     bot.send_message(message.chat.id, "Так вы и не входили, вы чего?.")
    # else:
    #     bot.send_message(message.chat.id, "Вы успешно вышли из аккаунта.")

    try:
        Db.pop(message.chat.id)
        bot.send_message(message.chat.id, "Вы успешно вышли из аккаунта.")
        me.setTOKEN('')
        send_menu(message)

    except KeyError:
        bot.send_message(message.chat.id, "Так вы и не входили, вы чего?.")
    # print("Хуек торчит")
    # me.setTOKEN('')
    # client = Client().init()


@bot.message_handler(commands=['s'])
def search(message):
    msg = bot.send_message(message.chat.id, "Напишите, какой альбом или трек вы хотите найти, или отправьте ссылку:")
    bot.register_next_step_handler(msg, search2)


def search2(message):
    if message.text[:5] == "https" and "track" in message.text:
        audio_title = me.download_by_link(str(message.text[-9:]))
        audio = open(audio_title, "rb")
        bot.send_audio(message.chat.id, audio)
    elif message.text[:5] == "https" and "track" not in message.text:
        me.setAlbum(message.text[-9:])
        tracks = me.get_tracks_by_album()
        buttons = []
        for i in range(len(tracks)):
            buttons.append(types.InlineKeyboardButton(text=tracks[i].author + " " + tracks[i].title,
                                                      callback_data='i' + str(tracks[i].id)))
        keyboard = types.InlineKeyboardMarkup(row_width=1).add(*buttons)
        low_row = [
            types.InlineKeyboardButton(text="<-", callback_data="prev_al_tr"),
            types.InlineKeyboardButton(text=me.page, callback_data="curr_page_al_tr"),
            types.InlineKeyboardButton(text="->", callback_data="next_al_tr")
        ]
        low_links = [
            types.InlineKeyboardButton(text="creator 1", url="https://github.com/yofujitsu"),
            types.InlineKeyboardButton(text="creator 2", url="https://github.com/Ulquiorrashif"),
        ]
        keyboard.row(*low_row)
        keyboard.row(*low_links)
        bot.send_message(message.chat.id, text="Список треков альбома", reply_markup=keyboard)
    elif "https" not in message.text:
        q = me.search_res(message.text)
        bot.send_message(message.chat.id, q)
        q2 = me.search(message.text)
        if q2[0] == "трек":
            audio_title = me.download_by_link(q2[1].id)
            audio = open(audio_title, "rb")
            bot.send_audio(message.chat.id, audio)
        elif q2[0] == "альбом":
            me.setAlbum(q2[1].id)
            tracks = me.get_tracks_by_album()
            buttons = []
            for i in range(len(tracks)):
                buttons.append(types.InlineKeyboardButton(text=tracks[i].author + " " + tracks[i].title,
                                                          callback_data='i' + str(tracks[i].id)))
            keyboard = types.InlineKeyboardMarkup(row_width=1).add(*buttons)
            low_row = [
                types.InlineKeyboardButton(text="<-", callback_data="prev_al_tr"),
                types.InlineKeyboardButton(text=me.page, callback_data="curr_page_al_tr"),
                types.InlineKeyboardButton(text="->", callback_data="next_al_tr")
            ]
            low_links = [
                types.InlineKeyboardButton(text="creator 1", url="https://github.com/yofujitsu"),
                types.InlineKeyboardButton(text="creator 2", url="https://github.com/Ulquiorrashif"),
            ]
            keyboard.row(*low_row)
            keyboard.row(*low_links)
            bot.send_message(message.chat.id, text="Список треков альбома", reply_markup=keyboard)
        elif q2[0] == "исполнитель":
            me.setArtist(q2[1].id)
            tracks = me.get_tracks_by_artist()
            buttons = []
            for i in range(len(tracks)):
                buttons.append(types.InlineKeyboardButton(text=tracks[i].author + " " + tracks[i].title,
                                                          callback_data='i' + str(tracks[i].id)))
            keyboard = types.InlineKeyboardMarkup(row_width=1).add(*buttons)
            low_row = [
                types.InlineKeyboardButton(text="<-", callback_data="prev_al_tr"),
                types.InlineKeyboardButton(text=me.page, callback_data="curr_page_al_tr"),
                types.InlineKeyboardButton(text="->", callback_data="next_al_tr")
            ]
            low_links = [
                types.InlineKeyboardButton(text="creator 1", url="https://github.com/yofujitsu"),
                types.InlineKeyboardButton(text="creator 2", url="https://github.com/Ulquiorrashif"),
            ]
            keyboard.row(*low_row)
            keyboard.row(*low_links)
            bot.send_message(message.chat.id, text="Список лучших треков исполнителя", reply_markup=keyboard)
        else:
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
                                                  callback_data='i' + str(tracks_titles[i].id)))
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
    for button in buttons: print(button.callback_data)


@bot.callback_query_handler(func=lambda call: "_pl_" in call.data)
def playlists_tracks_query_handler(call: types.CallbackQuery):
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
    if call.data == "prev_pl_tr" and me.page > 1:
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


@bot.callback_query_handler(func=lambda call: call.data.startswith("#P"))
def playlists_query_handler(call: types.CallbackQuery):
    try:
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
    except Exception as e:
        print("хуй там")


@bot.callback_query_handler(func=lambda call: "_al" in call.data)
def albums_tracks_query_handler(call: types.CallbackQuery):
    if call.data == "next_al_tr":
        # me.page+=1
        tracks_titles = me.get_tracks_by_album(1)
        buttons = []
        for i in range(len(tracks_titles)):
            buttons.append(types.InlineKeyboardButton(text=tracks_titles[i].author + " " + tracks_titles[i].title,
                                                      callback_data='i' + str(tracks_titles[i].id)))
        keyboard = types.InlineKeyboardMarkup(row_width=1).add(*buttons)
        low_row = [
            types.InlineKeyboardButton(text="<-", callback_data="prev_al_tr"),
            types.InlineKeyboardButton(text=me.page, callback_data="curr_page_al_tr"),
            types.InlineKeyboardButton(text="->", callback_data="next_al_tr")
        ]
        low_links = [
            types.InlineKeyboardButton(text="creator 1", url="https://github.com/yofujitsu"),
            types.InlineKeyboardButton(text="creator 2", url="https://github.com/Ulquiorrashif"),
        ]
        keyboard.row(*low_row)
        keyboard.row(*low_links)
        bot.send_message(call.message.chat.id, text="Список аудиозаписей из альбома", reply_markup=keyboard)
    if call.data == "prev_al_tr" and me.page > 1:
        # me.page-=1
        tracks_titles = me.get_tracks_by_album(-1)
        buttons = []
        for i in range(len(tracks_titles)):
            buttons.append(types.InlineKeyboardButton(text=tracks_titles[i].author + " " + tracks_titles[i].title,
                                                      callback_data='i' + str(tracks_titles[i].id)))
        keyboard = types.InlineKeyboardMarkup(row_width=1).add(*buttons)
        low_row = [
            types.InlineKeyboardButton(text="<-", callback_data="prev_al_tr"),
            types.InlineKeyboardButton(text=me.page, callback_data="curr_page_al_tr"),
            types.InlineKeyboardButton(text="->", callback_data="next_al_tr")
        ]
        low_links = [
            types.InlineKeyboardButton(text="creator 1", url="https://github.com/yofujitsu"),
            types.InlineKeyboardButton(text="creator 2", url="https://github.com/Ulquiorrashif"),
        ]
        keyboard.row(*low_row)
        keyboard.row(*low_links)
        bot.send_message(call.message.chat.id, text="Список аудиозаписей из альбома", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith("A"))
def albums_query_handler(call: types.CallbackQuery):
    try:
        me.setAlbum(call.data[1:])
        print(call.data[1:])
        tracks = me.get_tracks_by_album()
        buttons = []
        for i in range(len(tracks)):
            buttons.append(types.InlineKeyboardButton(text=tracks[i].author + " " + tracks[i].title,
                                                      callback_data='i' + str(tracks[i].id)))
        keyboard = types.InlineKeyboardMarkup(row_width=1).add(*buttons)
        low_row = [
            types.InlineKeyboardButton(text="<-", callback_data="prev_al_tr"),
            types.InlineKeyboardButton(text=me.page, callback_data="curr_page_al_tr"),
            types.InlineKeyboardButton(text="->", callback_data="next_al_tr")
        ]
        low_links = [
            types.InlineKeyboardButton(text="creator 1", url="https://github.com/yofujitsu"),
            types.InlineKeyboardButton(text="creator 2", url="https://github.com/Ulquiorrashif"),
        ]
        keyboard.row(*low_row)
        keyboard.row(*low_links)
        bot.send_message(call.message.chat.id, text="Список треков альбома", reply_markup=keyboard)
    except Exception as e:
        print("хуй там")


@bot.callback_query_handler(func=lambda call: "_my" in call.data )
def tracks_switch_query_handler(call: types.CallbackQuery):
    # ЗДЕСЬ ОШИБКА
    if call.data == "next_my1":
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
    if call.data == "prev_my" and me.page > 1:
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


@bot.callback_query_handler(func=lambda call: call.data.startswith("i"))
def tracks_query_handler(call: types.CallbackQuery):
    try:
        print(type(call.data))
        audio_title = me.download(str(call.data[1:]))
        lastId = call.data[1:]
        audio = open(audio_title, "rb")
        # bot.send_message(call.message.chat.id, call.data)
        bot.send_audio(call.message.chat.id, audio)
        # button = types.InlineKeyboardButton(text="Добавить трек в Мне нравится?", callback_data="favv")
        # keyboard_fav = types.InlineKeyboardMarkup().add(button)
        # low_row = [
        #     types.InlineKeyboardButton(text="Да", callback_data=call.data[1:] + "add"),
        #     types.InlineKeyboardButton(text="Нет", callback_data=call.data[1:] + "not")
        # ]
        # keyboard_fav.row(*low_row)
        # bot.send_message(call.message.chat.id, text="Похоже, что этот трек вам понравился...",
        #                  reply_markup=keyboard_fav)
    except Exception as e:
        print("фиг там")


@bot.callback_query_handler(func=lambda call: "add" in call.data)
def add_query_handler(call: types.CallbackQuery):
    res = me.add_to_favs(int(call.data[:-3]))
    if res == True:
        me.add_to_favs(int(call.data[:-3]))
        bot.send_message(call.message.chat.id, text="Трек добавлен в Мне нравится!")
    else:
        bot.send_message(call.message.chat.id, text="Трек уже находится в Мне нравится!")


@bot.callback_query_handler(func=lambda call: "not" in call.data)
def not_add_query_handler(call: types.CallbackQuery):
    bot.send_message(call.message.chat.id,
                     text="Не беда, в Яндекс.Музыке есть миллионы других треков, которые могут вам понравиться!")


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


@bot.message_handler(commands=['a'])
def my_albums(message):
    al = me.get_albums()
    buttons = [
        # types.InlineKeyboardButton(text=track.titles[0], callback_data="track_1"),
        # types.InlineKeyboardButton(text="track 2", callback_data="track_2"),
        # types.InlineKeyboardButton(text="track 3", callback_data="track_3"),
        # types.InlineKeyboardButton(text="track 4", callback_data="track_4"),
        # types.InlineKeyboardButton(text="track 5", callback_data="track_5")
    ]
    for i in range(len(al)):
        buttons.append(types.InlineKeyboardButton(text=al[i][0] + " - " + al[i][1],
                                                  callback_data='A' + str(al[i][2])))
    keyboard = types.InlineKeyboardMarkup(row_width=1).add(*buttons)
    low_row = [
        types.InlineKeyboardButton(text="<-", callback_data="prev_al"),
        types.InlineKeyboardButton(text=me.page, callback_data="curr_page_al"),
        types.InlineKeyboardButton(text="->", callback_data="next_al")
    ]
    low_links = [
        types.InlineKeyboardButton(text="creator 1", url="https://github.com/yofujitsu"),
        types.InlineKeyboardButton(text="creator 2", url="https://github.com/Ulquiorrashif"),
    ]
    keyboard.row(*low_row)
    keyboard.row(*low_links)

    bot.send_message(message.chat.id, text="Список добавленных альбомов", reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def bebra(message):
    try:
        me.setTOKEN(Db[message.chat.id])
    except KeyError:
        if (message.text == "menu"):
            send_menu(message)

        elif (message.text == "help"):
            bot.send_message(message.chat.id,
                             text="Привет! Я телеграм-бот, который поможет тебе скачать твою музыку из стриминговой платформы Яндекс.Музыка. С моей помощью ты сможешь:"
                                  "получать музыку из плейлиста 'Мне нравится', а также добавлять туда треки из других источников; получать музыку из добавленных альбомов и собственных плейлистов. "
                                  "Для доступа к этим данным тебе необходимо авторизоваться. Список команд доступен по кнопке слева в чате. Сила в музыке! ")

        elif (message.text == "Что я могу?"):
            bot.send_message(message.chat.id,
                             text="Привет! Я телеграм-бот, который поможет тебе скачать твою музыку из стриминговой платформы Яндекс.Музыка. С моей помощью ты сможешь:"
                                  "получать музыку из плейлиста 'Мне нравится', а также добавлять туда треки из других источников; получать музыку из добавленных альбомов и собственных плейлистов. "
                                  "Для доступа к этим данным тебе необходимо авторизоваться. Пиши /auth, чтобы авторизоваться. Сила в музыке! ")

        #ЗДЕСЬ ОШИБКА
        elif (message.text == "Вернуться в главное меню!"):
            bot.send_message(message.chat.id, text="Beep-beep... -_-", reply_markup=None)
            hello(message)

        elif message.text == "Войти":
            auth(message)
        else:
            bot.send_message(message.chat.id, "Функция недоступна, пока ТЫ не авторизуешься.")
    else:
        if (message.text == "menu"):
            send_menu(message)

        elif (message.text == "help"):
            bot.send_message(message.chat.id,
                             text="Привет! Я телеграм-бот, который поможет тебе скачать твою музыку из стриминговой платформы Яндекс.Музыка. С моей помощью ты сможешь:"
                                  "получать музыку из плейлиста 'Мне нравится', а также добавлять туда треки из других источников; получать музыку из добавленных альбомов и собственных плейлистов. "
                                  "Для доступа к этим данным тебе необходимо авторизоваться. Список команд доступен по кнопке слева в чате. Сила в музыке! ")

        elif (message.text == "Что я могу?"):
            bot.send_message(message.chat.id,
                             text="Привет! Я телеграм-бот, который поможет тебе скачать твою музыку из стриминговой платформы Яндекс.Музыка. С моей помощью ты сможешь:"
                                  "получать музыку из плейлиста 'Мне нравится', а также добавлять туда треки из других источников; получать музыку из добавленных альбомов и собственных плейлистов. "
                                  "Для доступа к этим данным тебе необходимо авторизоваться. Пиши /auth, чтобы авторизоваться. Сила в музыке! ")

        elif (message.text == "Вернуться в главное меню!"):
            bot.send_message(message.chat.id, text="Beep-beep... -_-", reply_markup=None)
            hello(message)

        elif message.text == "Войти":
            bot.send_message(message.chat.id, "Вы уже вошли в свой аккаунт!")

        elif (message.text == "Мне нравится"):
            cmd_inline_url(message)

        elif message.text == "Выйти":
            unauth(message)

        elif message.text == 'Музыка из моих плейлистов':
            my_playlists(message)

        elif message.text == "Музыка из моих альбомов":
            my_albums(message)

        elif message.text == "Поиск":
            search(message)
        # if me.getTOKEN() == "":
        #     if (message.text == "menu"):
        #         send_menu(message)
        #
        #     elif (message.text == "help"):
        #         bot.send_message(message.chat.id,
        #                          text="Привет! Я телеграм-бот, который поможет тебе скачать твою музыку из стриминговой платформы Яндекс.Музыка. С моей помощью ты сможешь:"
        #                               "получать музыку из плейлиста 'Мне нравится', а также добавлять туда треки из других источников; получать музыку из добавленных альбомов и собственных плейлистов. "
        #                               "Для доступа к этим данным тебе необходимо авторизоваться. Список команд доступен по кнопке слева в чате. Сила в музыке! ")
        #
        #     elif (message.text == "Что я могу?"):
        #         bot.send_message(message.chat.id,
        #                          text="Привет! Я телеграм-бот, который поможет тебе скачать твою музыку из стриминговой платформы Яндекс.Музыка. С моей помощью ты сможешь:"
        #                               "получать музыку из плейлиста 'Мне нравится', а также добавлять туда треки из других источников; получать музыку из добавленных альбомов и собственных плейлистов. "
        #                               "Для доступа к этим данным тебе необходимо авторизоваться. Пиши /auth, чтобы авторизоваться. Сила в музыке! ")
        #
        #     elif (message.text == "Вернуться в главное меню"):
        #         bot.send_message(message.chat.id, text="Beep-beep... -_-", reply_markup=None)
        #         hello(message)
        #
        #     elif message.text == "Войти":
        #         auth(message)
        #     else:
        #         bot.send_message(message.chat.id, "Функция недоступна, пока ТЫ не авторизуешься.")
        # else:
        #
        #     if (message.text == "menu"):
        #         send_menu(message)
        #
        #     elif (message.text == "help"):
        #         bot.send_message(message.chat.id,
        #                          text="Привет! Я телеграм-бот, который поможет тебе скачать твою музыку из стриминговой платформы Яндекс.Музыка. С моей помощью ты сможешь:"
        #                               "получать музыку из плейлиста 'Мне нравится', а также добавлять туда треки из других источников; получать музыку из добавленных альбомов и собственных плейлистов. "
        #                               "Для доступа к этим данным тебе необходимо авторизоваться. Список команд доступен по кнопке слева в чате. Сила в музыке! ")
        #
        #     elif (message.text == "Что я могу?"):
        #         bot.send_message(message.chat.id,
        #                          text="Привет! Я телеграм-бот, который поможет тебе скачать твою музыку из стриминговой платформы Яндекс.Музыка. С моей помощью ты сможешь:"
        #                               "получать музыку из плейлиста 'Мне нравится', а также добавлять туда треки из других источников; получать музыку из добавленных альбомов и собственных плейлистов. "
        #                               "Для доступа к этим данным тебе необходимо авторизоваться. Пиши /auth, чтобы авторизоваться. Сила в музыке! ")
        #
        #     elif (message.text == "Вернуться в главное меню"):
        #         bot.send_message(message.chat.id, text="Beep-beep... -_-", reply_markup=None)
        #         hello(message)
        #
        #     elif message.text == "Войти":
        #         bot.send_message(message.chat.id, "Вы уже вошли в свой аккаунт!")
        #
        #     elif (message.text == "Мне нравится"):
        #         cmd_inline_url(message)
        #
        #     elif message.text == "Выйти":
        #         unauth(message)
        #
        #     elif message.text == 'Музыка из моих плейлистов':
        #         my_playlists(message)
        #
        #     elif message.text == "Музыка из моих альбомов":
        #         my_albums(message)
        #
        #     elif message.text == "Поиск":
        #         search(message)


async def main():
    await bot.polling(none_stop=True)


if __name__ == "__main__":
    # await bot.enable_save_next_step_handlers(delay=2)
    # await bot.load_next_step_handlers()
    asyncio.run(main())
    # with open('app.log', 'r') as log_file:
    #     log_data = log_file.read()
    #     print(log_data)

# executor.start_polling(dp, skip_updates=True)
