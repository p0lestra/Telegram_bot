import requests
import telebot
import json

TOKEN = '6276958231:AAF18JXrc5KaQ17TGcDk2CAFixjv-QaVg2U'
api = {
    "apikey": "eKR8tZwRbBYMot7PONndd8EZ5qVAn7vf"
}

bot = telebot.TeleBot(TOKEN)

keys = {
    'рубль': 'RUB',
    'доллар': 'USD',
    'евро': 'EUR'
}


@bot.message_handler(commands=['help', 'start'])
def helper(message: telebot.types.Message):
    text = 'Чтобы перевести нужную вам валюту, напишите сообщение в таком формате: \n <имя валюты> <имя валюты, в которой надо узнать цену первой валюты> <количество первой валюты>\
    \nУвидеть список всех доступных валют: /values'

    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    base, to, amount = message.text.split(' ')
    r = requests.get(
        f"https://api.apilayer.com/exchangerates_data/convert?to={keys[to]}&from={keys[base]}&amount={amount}", headers=api)
    total = json.loads(r.content)['result']
    print(f'{total}')
    text = f'Цена {amount} {base} в {to} = {total}'
    bot.send_message(message.chat.id, text)


bot.polling()
