# FromYandexMusicBot
![image](https://github.com/yofujitsu/tg_music_bot/assets/78373273/227f865d-cdc6-448c-992e-16baaad2f07e)

## Командный проект по курсу "Технологии разработки программных приложений" в РТУ МИРЭА
## Описание проекта
FromYandexMusicBot - это телеграм-бот, с помощью которого можно получить доступ к музыкальному каталогу "Яндекс.Музыка".
## Разработчики проекта
[Цветков Александр](https://github.com/yofujtsu) | [Тригубов Родион](https://github.com/Ulquiorrashif)

1. Функциональные требования к продукту:
    - Удобное меню
    - Поиск треков по названию / ссылке
    - Авторизация пользователя (ручная)
    - Скачивание треков из собственных плейлистов, альбомов, избранного (плейлиста "Мне нравится"). 

2. Портрет пользователя:
    - Пользователь - молодой человек, активно слушающий музыку на стриминговом сервисе "Яндекс.Музыка", пользующийся мессенджером "Telegram".

3. Требования к продукту:
    + Требования к клиентской части сервиса
      - Приятный и современный внешний вид 
      - Понятный интерфейс
      - Кнопки для команд
      - Обновляющийся список песен
    + Функциональные требования
      - Все запросы должны завершаться меньше чем за 1 секунду
      - Сервис должен быть доступен удаленно
      - Сервис не должен сохранять данные пользователей (для этого реализована функция выхода из аккаунта)
 
## Технологии проекта
   + Python — Высокоуровневый язык программирования, который обладает простым синтаксисом и читабельностью, является очень популярным языком программирования и содержит множество библиотек для комфортной разработки telegram-ботов
   + Telegram API — это API, через который ваше telegram-приложение связывается с сервером. Telegram API полностью открыт, так что любой разработчик может написать свой клиент мессенджера.
   + Yandex Music API - это неофициальное API, через который telegram-приложение связывается с аккаунтом Yandex. В этом API реализованы методы и клиент для удобной работы с треками, плейлистами и поиском.
   + Docker. Программная платформа, которая позволяет разработчикам быстро создавать, тестировать и развертывать контейнерные приложения.


## Установка зависимостей
Для единовременной загрузки всех необходимых для проекта зависимостей был прописан конфигурационный файл requirements.txt. В нем прописаны все необходимые для проекта зависимости и их версии (а также API telebot, aiogram и yandex-music). При открытии проекта в IDE вам будет предложено установить все недостающие зависимости. Это достаточно удобно, нежели вводить pip install для каждой библиотеки вручную.

![image](https://github.com/yofujitsu/tg_music_bot/assets/78373273/5f997ee1-d46e-4050-a969-86a9ac5f035e)

Также в проекте находится сборочный файл setup.py. Прописав команду python setup.py sdist можно собрать проект в пакет и использовать как библиотеку:
```
python setup.py sdist
pip install tg_music_bot.tar.gz
import tg_music_bot
```

## Запуск бота
Чтобы запустить бота на локальном уровне необходимо перейти в директорию с проектом и прописать следующую команду в терминале:
```
python bot.py
```

## Внешний вид сервиса
### Страница диалога с ботом в telegram
### Бота можно найти по ссылке https://t.me/fromvkmusicbot
![image](https://github.com/yofujitsu/tg_music_bot/assets/78373273/7e2d0f10-a87d-49fa-b670-46048dc3bc06)


## Мануал по кнопкам
### Боковое меню
Слева в поле ввода сообщения можно найти кнопку, по нажатию которой откроется контекстное меню с командами, которые поддерживает бот-сервис.
## Боковое меню
![image](https://github.com/yofujitsu/tg_music_bot/assets/78373273/d45e01bd-2265-4a97-a386-ec6e7b458d18)



## Мануал по командам
### Команда /start
Команда /start запускает работу бота и открывает меню из двух кнопок: "menu" и "help"
![image](https://github.com/yofujitsu/tg_music_bot/assets/78373273/c8fad584-510c-4e4a-9de0-f540f81536ea)

