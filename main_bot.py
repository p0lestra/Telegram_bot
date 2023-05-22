import telebot

TOKEN = '6276958231:AAF18JXrc5KaQ17TGcDk2CAFixjv-QaVg2U'

bot = telebot.TeleBot(TOKEN)

keys = {
    'рубль': 'RUB',
    'доллар': 'USD',
    'евро': 'EUR'
}


@bot.message_handler(commands=['help', 'start'])
def helper(message: telebot.types.Message):
    text = 'Чтобы перевести нужную вам валюту, напишите сообщение в таком формате: \n <валюта> <в какую валюту перевести> <колво переводимой валюты>'

    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


bot.polling()
