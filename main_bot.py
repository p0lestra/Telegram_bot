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


class APIException(Exception):
    pass


class MoneyConverter:
    @staticmethod
    def convert(to: str, base: str, amount: str):
        if to == base:
            raise APIException(f'Не удалось перевести одинаковые валюты {base}')

        try:
            to_ticker = keys[to]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {to}')
        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}')
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}')

        r = requests.get(
            f"https://api.apilayer.com/exchangerates_data/convert?to={to_ticker}&from={base_ticker}&amount={amount}",
            headers=api)
        total = json.loads(r.content)['result']
        print(f'{total}')

        return total


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
    parametrs = message.text.split(' ')

    if len(parametrs) != 3:
        raise APIException('Слишком много значений')
    base, to, amount = parametrs

    total = MoneyConverter.convert(to, base, amount)
    text = f'Цена {amount} {base} в {to} = {total}'
    bot.send_message(message.chat.id, text)


bot.polling()
