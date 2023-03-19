import vk_api
from vk_api import audio
import requests
from time import time
import os
REQUEST_STATUS_CODE = 200

# Данные левого акка, чтобы api работал
# можно не менять
login = 'your_login'  # Номер телефона
password = 'your_pswrd'  # Пароль
my_id = 'your_id' # Ваш id

path = r'C:\Users\sesa7\Desktop\media\music\mp3'  # Нужно прописать путь,куда скачают файлы

def auth_handler():
    """ При двухфакторной аутентификации вызывается эта функция.
    """

    # Код двухфакторной аутентификации
    key = input("Enter authentication code: ")
    # Если: True - сохранить, False - не сохранять.
    remember_device = True

    return key, remember_device

if not os.path.exists(path):
    os.makedirs(path)

vk_session = vk_api.VkApi(
        login, password,
        # функция для обработки двухфакторной аутентификации
        auth_handler=auth_handler
    )

try:
    vk_session.auth()
except vk_api.AuthError as error_msg:
    print(error_msg)

vk = vk_session.get_api()
vk_audio = audio.VkAudio(vk_session)

os.chdir(path)

i = vk_audio.get(owner_id=my_id)[0]
r = requests.get(i["url"])
if r.status_code == REQUEST_STATUS_CODE:
    try:
        with open(i["artist"] + '_' + i["title"] + '.mp3', 'wb') as output_file:
            output_file.write(r.content)
    except OSError:
        with open(i["artist"] + '_' + i["title"] + '.mp3', 'wb') as output_file:
            output_file.write(r.content)
a = 0
time_start = time()
for i in vk_audio.get(owner_id=my_id):
    try:
        a += 1
        r = requests.get(i["url"])
        if r.status_code == REQUEST_STATUS_CODE:
            with open(i["artist"] + '_' + i["title"] + '.mp3', 'wb') as output_file:
                output_file.write(r.content)
    except OSError:
        print(a)
