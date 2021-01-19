import telebot
from config import TOKEN, keys
from extensions import ConvertException, ConvertionException

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = '\n\
    Чтобы начать работу бота, введите сообщение в следующем формате: \n <название валюты> \
    <валюту, в которую необходимо перевести> \
    <количество переводимой валюты>\n\
    Название валюты необходимо вводить в именительном падеже в единственном числе. ' \
    'Количество валюты вводить в целых числах, либо использовать в качестве разделителя точку.\n\
    Список доступных валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def values(message: telebot.types.Message):
    try:
        c = message.text.split(' ')

        if len(c) != 3:
            raise ConvertException('Введено неверное количество параметров')

        quote, base, amount = c
        quote = quote.lower()
        base = base.lower()
        value = ConvertionException.convert(quote, base, amount)
        b = value * float(amount)
    except ConvertException as e:
        bot.reply_to(message, e)
    except Exception as e:
        bot.reply_to(message, f'Не удалось выполнить команду {e}')
    else:
        text = f'Цена {amount} {quote} в {base} = {b}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
