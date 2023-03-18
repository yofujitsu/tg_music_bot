import setuptools
import random
import telebot
from telebot import types
import vk_api
import aiogram
import requests
from bs4 import BeautifulSoup as b

API_TOKEN = "5952876513:AAEG1jg7AiXYmPPx9U5_FraCq00HYEztkwE"

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def hello(message):
    bot.send_message(message.chat.id, text="""Привет! Если хочешь ознакомиться с командами - жми menu. Хочешь узнать, что делает каждая команда - жми help. Хочешь узнать какого бот о тебе мнения - пиши любое сообщение)""")
    markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("menu")
    btn2 = types.KeyboardButton("help")
    markup1.add(btn1, btn2)
    bot.send_message(message.chat.id, text="ну чо ёпта", reply_markup=markup1)

@bot.message_handler(commands=['my','rs','s','ps'])
def commands_rofl(message):
    bot.send_message(message.chat.id, "Уолтер, убери свой член подальше, Уолтер :(")

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
    bot.send_message(message.chat.id, text="ну чо ёпта", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def bebra(message):
    if (message.text == "menu"):
        send_menu(message)

    elif (message.text == "help"):
        bot.send_message(message.chat.id, text="а вот хуй те")

    elif (message.text == "Что я могу?"):
        bot.send_message(message.chat.id, "обоссать тебя и твою семью")

    elif message.text == any(["Музыка из профиля", "Музыка из плейлиста", "Музыка из чартов", "Музыка из рекомендаций",
                              "Общий поиск из базы"]):
        bot.send_message(message.chat.id, text="пока не готово. пшел нахуй.")

    elif (message.text == "Вернуться в главное меню"):
        bot.send_message(message.chat.id, text="waltuh... -_-", reply_markup=None)
        hello(message)
    else:
        bot.send_message(message.chat.id, text="не понимаю че пиздишь нах")

bot.polling()
