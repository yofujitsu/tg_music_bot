from setuptools import setup

setup(
    name='tg_music_bot_1',
    version='1.0',
    packages=['tg_music_bot_1'],
    url='https://github.com/yofujitsu/tg_music_bot',
    author='yofujitsu',
    author_email='yofujitsuuu@gmail.com',
    description='Yandex Music Telegram Bot',
    install_requires=[
        'yandex-music',
        'telebot',
        'aiogram',
        'requests',
        'setuptools'
    ],
)