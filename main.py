import telebot
from random import randint
import config as cfg
import requests
import json

client = telebot.TeleBot(cfg.token)


@client.message_handler(commands=['start'])
def start(message):
    print('[LOG] Used command `start`')
    client.send_message(message.chat.id, 'Бот может выводить случайные картинки по запросу /image или /random_image\nПосле команды можно указать что конкретно вы хотите найти (/pictures)')


@client.message_handler(commands=['pictures'])
def pictures(message):
    print('[LOG] Used command `pictures`')
    client.send_message(message.chat.id, 'Список всех доступных изображений:\ndog\ncat\npanda\nfox\nkoala\nbird\nraccoon\nkangaroo')


@client.message_handler(commands=['random_image', 'ri', 'image'])
def image(message):
    params = message.text
    print(f'[LOG] Used command `image` with args: {params}')
    if len(params.split(' ')) == 1:
        arg = 'dog'
    else:
        arg = params.split(' ')[1].lower()
    url = 'https://some-random-api.ml/img/' + str(arg)
    response = requests.get(url)
    if response.status_code != 404:
        text = response.text
        context = json.loads(text)
        img = context['link']
        client.send_photo(message.chat.id, img)
    else:
        client.send_message(message.chat.id, 'Данное фото не найдено\nСписок доступных изображений: /pictures')


client.polling(none_stop=True, interval=0)
