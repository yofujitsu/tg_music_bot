import vk_api
from vk_api import audio
import requests
from time import time
import os


REQUEST_STATUS_CODE = 200

# Данные левого акка, чтобы api работал
# можно не менять
login = '+79966289022'  # Номер телефона
password = 'Qwerty12345*'  # Пароль
my_id = '790690401' # Ваш id

path = r'C:\Users\rodio\OneDrive\Рабочий стол\m'  # Нужно прописать путь,куда скачают файлы

if not os.path.exists(path):
    os.makedirs(path)

vk_session = vk_api.VkApi(login=login, password=password)
vk_session.auth()
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