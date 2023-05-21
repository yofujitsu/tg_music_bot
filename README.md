# FromYandexMusicBot
## Командный проект по курсу "Технологии разработки программных приложений" в РТУ МИРЭА
## Описание проекта
FromYandexMusicBot - это телеграм-бот, с помощью которого можно получить доступ к музыкальному каталогу "Яндекс.Музыка".

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
    $ pip install yandex-music
    $ pip install telebot


## Внешний вид сервиса
### Страница диалога с ботом в telegram
![image](https://github.com/yofujitsu/tg_music_bot/assets/78373273/6d3dff07-08e5-49bb-899d-2855a77a4ce2)
