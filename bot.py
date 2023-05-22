import setuptools
import random
import telebot
from telebot import types
from aiogram.types import *
import aiogram
import requests
from bs4 import BeautifulSoup as b
from yandex_music import Client
from yandex_music.exceptions import UnauthorizedError

from yandex_parser import MyPerson

client = Client().init()
#'y0_AgAAAAA-m1eKAAG8XgAAAADjdu60-k8-pH7FQ2u9v4GHmaRAFx_JP60'
#'AQAAAAASg-EiAAG8Xth12jSrvkhtqzxHtyTafzo'
API_TOKEN = "5952876513:AAEG1jg7AiXYmPPx9U5_FraCq00HYEztkwE"
lastId = 0

bot = telebot.TeleBot(API_TOKEN)

me = MyPerson()

@bot.message_handler(commands=['start'])
def hello(message):
    markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("menu")
    btn2 = types.KeyboardButton("help")
    markup1.add(btn1, btn2)
    bot.send_message(message.chat.id, text="""Привет! Если хочешь ознакомиться с командами - жми menu. Хочешь узнать, что делает каждая команда - жми help.""", reply_markup=markup1)


@bot.message_handler(commands=['help'])
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
    if me.getTOKEN() == '':
        msg = bot.send_message(message.chat.id,
                               "Для входа в аккаунт вам необходимо ввести Токен. Шпаргалка по получению токена доступна по ссылке ниже. Вы должны прислать строку без кавычек! Не бойтесь, мы не крадем ваши персональные данные, токен используется лишь для доступа к музыкальному каталогу пользователя.")
        bot.send_message(message.chat.id, "https://yandex-music.readthedocs.io/en/main/token.html")
        bot.register_next_step_handler(msg, auth2)
    else: bot.send_message(message.chat.id, "Вы уже вошли с свой аккаунт!")

def auth2(message):
    try:
        me.setTOKEN(message.text)
        client = Client(message.text).init()
        bot.send_message(message.chat.id, "Вы успешно вошли в аккаунт!")
        send_menu(message)
    except UnauthorizedError or UnicodeEncodeError:
        me.setTOKEN('')
        client = Client().init()
        bot.send_message(message.chat.id, "Вы ввели невалидный токен. Внимательно прочитайте мануал. Пишите /auth для повторной попытки.")

@bot.message_handler(commands=['exit'])
def unauth(message):
    if me.getTOKEN() == '':
        bot.send_message(message.chat.id, "Так вы и не входили, вы чего?.")
    else:
        bot.send_message(message.chat.id, "Вы успешно вышли из аккаунта.")
        me.setTOKEN('')
        client = Client().init()
        send_menu(message)

@bot.message_handler(commands=['s'])
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
        lastId = call.data[1:]
        print(lastId)
        audio = open(audio_title, "rb")
        # bot.send_message(call.message.chat.id, call.data)
        bot.send_audio(call.message.chat.id, audio)
        button = types.InlineKeyboardButton(text="Добавить трек в Мне нравится?", callback_data="favv")
        keyboard_fav = types.InlineKeyboardMarkup().add(button)
        low_row = [
            types.InlineKeyboardButton(text="Да", callback_data=call.data[1:]+"add"),
            types.InlineKeyboardButton(text="Нет", callback_data=call.data[1:]+"not")
        ]
        keyboard_fav.row(*low_row)
        bot.send_message(call.message.chat.id, text="Похоже, что этот трек вам понравился...", reply_markup=keyboard_fav)
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
    if call.data[0] == "A":
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
    if "add" in call.data:
        res = me.add_to_favs(int(call.data[:-3]))
        if res == True:
            me.add_to_favs(int(call.data[:-3]))
            bot.send_message(call.message.chat.id, text="Трек добавлен в Мне нравится!")
        else:
            bot.send_message(call.message.chat.id, text="Трек уже находится в Мне нравится!")
    if "not" in call.data:
        bot.send_message(call.message.chat.id, text="Не беда, в Яндекс.Музыке есть миллионы других треков, которые могут вам понравиться!")
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
    if call.data == "prev_al_tr" and me.page>1:
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
    if me.getTOKEN() =="":
        if (message.text == "menu"):
            send_menu(message)

        elif (message.text == "help"):
            bot.send_message(message.chat.id,
                             text="Привет! Я телеграм-бот, который поможет тебе скачать твою музыку из стриминговой платформы Яндекс.Музыка. С моей помощью ты сможешь:"
                                  "получать музыку из плейлиста 'Мне нравится', а также добавлять туда треки из других источников; получать музыку из добавленных альбомов и собственных плейлистов. "
                                  "Для доступа к этим данным тебе необходимо авторизоваться. Список команд доступен по кнопке слева в чате. Сила в музыке! ")

        elif (message.text == "Что я могу?"):
            bot.send_message(message.chat.id, text="Привет! Я телеграм-бот, который поможет тебе скачать твою музыку из стриминговой платформы Яндекс.Музыка. С моей помощью ты сможешь:"
                                                   "получать музыку из плейлиста 'Мне нравится', а также добавлять туда треки из других источников; получать музыку из добавленных альбомов и собственных плейлистов. "
                                                   "Для доступа к этим данным тебе необходимо авторизоваться. Пиши /auth, чтобы авторизоваться. Сила в музыке! ")

        elif (message.text == "Вернуться в главное меню"):
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
            bot.send_message(message.chat.id, text="Привет! Я телеграм-бот, который поможет тебе скачать твою музыку из стриминговой платформы Яндекс.Музыка. С моей помощью ты сможешь:"
                                                   "получать музыку из плейлиста 'Мне нравится', а также добавлять туда треки из других источников; получать музыку из добавленных альбомов и собственных плейлистов. "
                                                   "Для доступа к этим данным тебе необходимо авторизоваться. Пиши /auth, чтобы авторизоваться. Сила в музыке! ")

        elif (message.text == "Вернуться в главное меню"):
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
            msg = bot.send_message(message.chat.id, "Напишите, что хотите найти:")
            bot.register_next_step_handler(msg, search2)

bot.polling()
