import telebot
from telebot import types
from datetime import datetime
with open("token.txt", "r") as f:
    token = f.read()
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(commands=['help'])
def send_welcome(message):
	bot.reply_to(message, "to add new record type '/add'")

@bot.message_handler(commands=['add'])
def add(message):
    splitted = message.text.split(' ')
    if len(splitted) != 3:
        bot.reply_to(message, "/add cost name")
    else:
        file = open('data/' + str(message.chat.id) + '.csv', 'a+')
        # file.write(str(splitted[1:]))
        file.write(str(datetime.now()) + ', ' + ', '.join(splitted[1:]) + "\n")
        file.close()
    mainmenu = types.InlineKeyboardMarkup()
    key1 = types.InlineKeyboardButton(text='кофе', callback_data='key1')
    key2 = types.InlineKeyboardButton(text='ост', callback_data='key2')
    mainmenu.add(key1, key2)
    bot.send_message(message.chat.id, 'choose category', reply_markup=mainmenu)


    #bot.send_message(message.chat.id, "What do you want to add?")


@bot.message_handler(commands=['excel'])
def send_welcome(message):
    with open('./data/' + str(message.chat.id) + '.csv') as doc:
	    bot.send_document(message.chat.id, doc)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
	bot.reply_to(message, message.text)

bot.infinity_polling()