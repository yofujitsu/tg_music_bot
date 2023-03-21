import os
import m3u8
import requests
from vk_api import VkApi
from vk_api.audio import VkAudio
from vk_api.audio import VkAudio
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import unpad


class M3U8Downloader:

    def __init__(self, login: str, password: str):

        self._vk_session = VkApi(
            login=login,
            password=password,
            api_version='5.81'
        )
        self._vk_session.auth()

        self._vk_audio = VkAudio(self._vk_session)

    def download_audio(self, q: str):
        url = self._get_audio_url(q=q)
        segments = self._get_audio_segments(url=url)
        segments_data = self._parse_segments(segments=segments)
        segments = self._download_segments(segments_data=segments_data, index_url=url)
        self._convert_ts_to_mp3(segments=segments)

    @staticmethod
    def _convert_ts_to_mp3(segments: bytes):
        with open(f'media/music/segments/temp.ts', 'w+b') as f:
            f.write(segments)
        os.system(f'ffmpeg -i "media/music/segments/temp.ts" -vcodec copy '
                  f'-acodec copy -vbsf h264_mp4toannexb "media/music/mp3/temp.wav"')
        os.remove("../m3u8_downloader/segments/temp.ts")

    def _get_audio_url(self, q: str):
        self._vk_audio.get_albums_iter()
        audio = next(self._vk_audio.search_iter(q=q))
        url = audio['url']
        return url

    @staticmethod
    def _get_audio_segments(url: str):
        m3u8_data = m3u8.load(
            uri=url
        )
        return m3u8_data.data.get("segments")

    @staticmethod
    def _parse_segments(segments: list):
        segments_data = {}

        for segment in segments:
            segment_uri = segment.get("uri")

            extended_segment = {
                "segment_method": None,
                "method_uri": None
            }
            if segment.get("key").get("method") == "AES-128":
                extended_segment["segment_method"] = True
                extended_segment["method_uri"] = segment.get("key").get("uri")
            segments_data[segment_uri] = extended_segment
        return segments_data

    @staticmethod
    def download_key(key_uri: str) -> bin:
        return

    @staticmethod
    def _download_segments(segments_data: dict, index_url: str) -> bin:
        downloaded_segments = []

        for uri in segments_data.keys():
            audio = requests.get(url=index_url.replace("index.m3u8", uri))

            downloaded_segments.append(audio.content)

            if segments_data.get(uri).get("segment_method") is not None:
                key_uri = segments_data.get(uri).get("method_uri")
                key = requests.get(url=key_uri).content

                iv = downloaded_segments[-1][0:16]
                ciphered_data = downloaded_segments[-1][16:]

                cipher = AES.new(key, AES.MODE_CBC, iv=iv)
                data = unpad(cipher.decrypt(ciphered_data), AES.block_size)
                downloaded_segments[-1] = data

        return b''.join(downloaded_segments)




login = '+79966289022'  # Номер телефона
password = 'Qwerty12345*'  # Пароль
my_id = '790690401' # Ваш id
md = M3U8Downloader(login=login, password=password)

q = "Воллны Волны"  # Запрос музыки по названию
md.download_audio(q)