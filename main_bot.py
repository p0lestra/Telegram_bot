import telebot
from config import TOKEN, keys
from extensions import APIException, MoneyConverter

bot = telebot.TeleBot(TOKEN)


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
    try:
        parametrs = message.text.split(' ')

        if len(parametrs) != 3:
            raise APIException('Слишком много значений')
        base, to, amount = parametrs
        total = MoneyConverter.get_price(to, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать комманду.\n{e}')
    else:
        text = f'Цена {amount} {base} в {to} = {total}'
        bot.send_message(message.chat.id, text)


bot.polling()
