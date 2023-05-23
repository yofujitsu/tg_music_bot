FROM python:latest
COPY . .
RUN pip install -r requirements.txt
CMD python tg_music_bot/bot.py