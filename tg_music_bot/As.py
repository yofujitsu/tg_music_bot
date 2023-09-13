# # # from yandex_music import ClientAsync
# # #
# # # async def main():
# # #     token = 'AQAAAAASg-EiAAG8Xth12jSrvkhtqzxHtyTafzo'
# # #     client = ClientAsync(token)
# # #     await client.init()
# # #     print(await client.users_likes_tracks())
# # # await main()
# # import asyncio
# # from yandex_music import ClientAsync
# #
# # from tg_music_bot import MyPerson
# #
# #
# # async def main():
# #     token = 'AQAAAAASg-EiAAG8Xth12jSrvkhtqzxHtyTafzo'
# #     client = ClientAsync(token)
# #     await client.init()
# #     print(await client.users_likes_tracks())
# # #
# # # class MyAsyncPerson(MyPerson):
# # #     def __init__(self):
# # #         self.client = ClientAsync().init
# # #
# # #     async def setTOKEN(self, TOKEN):
# # #         self.TOKEN = TOKEN
# # #
# # #         self.client = ClientAsync(TOKEN)
# # #         await self.client.init()
# #
# # if __name__ == '__main__':
# #     loop = asyncio.get_event_loop()
# #     loop.run_until_complete(main())
# import asyncio
# import logging
# import sys
# from os import getenv
#
# from aiogram import Bot, Dispatcher, Router, types
# from aiogram.enums import ParseMode
# from aiogram.filters import CommandStart, Command
# from aiogram.types import Message
# from aiogram.utils.markdown import hbold
#
# # Bot token can be obtained via https://t.me/BotFather
# from yandex_music.exceptions import UnauthorizedError
#
# from tg_music_bot import MyAsyncPerson
# class Database():
#     def __init__(self,userid,yid):
#         self.userid= userid
#         self.yid = yid
#
# TOKEN = "5952876513:AAEG1jg7AiXYmPPx9U5_FraCq00HYEztkwE"
#
# # All handlers should be attached to the Router (or Dispatcher)
# dp = Dispatcher()
# # me = MyAsyncPerson()
#
# @dp.message(CommandStart())
#
# async def command_start_handler(message: Message) -> None:
#     """
#     This handler receives messages with `/start` command
#     """
#     # Most event objects have aliases for API methods that can be called in events' context
#     # For example if you want to answer to incoming message you can use `message.answer(...)` alias
#     # and the target chat will be passed to :ref:`aiogram.methods.send_message.SendMessage`
#     # method automatically or call API method directly via
#     # Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`
#     await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")
# @dp.message(Command("auth"))
# async def auth(message:Message):
#     mas = message.text.split(' ')
#     tre.append(Database(message.from_user.id, mas[-1]))
#     # me=MyAsyncPerson()
#     # if me.getTOKEN() == '':
#     #     mas = message.text.split(' ')
#     #     tre.append(Database(message.from_user.id, me.client.token))
#         # if len(mas)>1:
#         #     try:
#         #         mas.append(Database(message.from_user.id,me.client.token))
#         #
#         #         await me.setTOKEN(mas[-1])
#         #         # client = Client(message.text).init()
#         #         await message.answer( "Вы успешно вошли в аккаунт!")
#         #         # print(await me.get_albums())
#         #         # send_menu(message)
#         #     except UnauthorizedError or UnicodeEncodeError:
#         #         await me.setTOKEN('')
#         #         # client = Client().init()
#         #         await message.answer( "Вы ввели невалидный токен. Внимательно прочитайте мануал. Пишите /auth для повторной попытки.")
#         # else:
#         #     await message.answer("Для входа в аккаунт вам необходимо ввести Токен. Шпаргалка по получению токена доступна по ссылке ниже. Вы должны прислать строку без кавычек! Не бойтесь, мы не крадем ваши персональные данные, токен используется лишь для доступа к музыкальному каталогу пользователя.")
#         #     await message.answer( "https://yandex-music.readthedocs.io/en/main/token.html")
#         # bot.
#         # bot.register_next_step_handler(msg,  auth2)
#
#     # else: await message.answer( "Вы уже вошли с свой аккаунт!")
#
#
# @dp.message(Command("my"))
# async def qwe(message:Message):
#     for i in tre:
#         if message.from_user.id == i.userid:
#             await me.setTOKEN(i.yid)
#             await message.answer(await me.get_playlists())
#         else:
#             await message.answer("Авторизуйся")
#
#
#
# # @dp.message()
# # async def echo_handler(message: types.Message) -> None:
# #     """
# #     Handler will forward receive a message back to the sender
# #
# #     By default, message handler will handle all message types (like a text, photo, sticker etc.)
# #     """
# #     try:
# #         # Send a copy of the received message
# #         await message.send_copy(chat_id=message.chat.id)
# #     except TypeError:
# #         # But not all the types is supported to be copied so need to handle it
# #         await message.answer("Nice try!")
#
# @dp.message(Command("menu"))
# async def echo_handler(message: types.Message) -> None:
#     """
#     Handler will forward receive a message back to the sender
#
#     By default, message handler will handle all message types (like a text, photo, sticker etc.)
#     """
#     try:
#         # Send a copy of the received message
#         await message.answer("Убери свой член")
#     except TypeError:
#         # But not all the types is supported to be copied so need to handle it
#         await message.answer("Пошел нахуй")
# @dp.message()
# async def echo_handler(message: types.Message) -> None:
#     """
#     Handler will forward receive a message back to the sender
#
#     By default, message handler will handle all message types (like a text, photo, sticker etc.)
#     """
#     try:
#         # Send a copy of the received message
#         await message.answer("Каждое сообщение")
#     except TypeError:
#         # But not all the types is supported to be copied so need to handle it
#         await message.answer("Пошел нахуй")
# async def main() -> None:
#     # Initialize Bot instance with a default parse mode which will be passed to all API calls
#
#     # And the run events dispatching
#     await dp.start_polling(bot)
#
#
# if __name__ == "__main__":
#     global bot
#     global me
#     global tre
#
#
#     tre = []
#     me = MyAsyncPerson()
#     bot =  Bot(TOKEN, parse_mode=ParseMode.HTML)
#     logging.basicConfig(level=logging.INFO, stream=sys.stdout)
#     asyncio.run(main())