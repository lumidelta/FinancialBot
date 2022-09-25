import telebot
with open("token.txt", "r") as f:
    token = f.read()
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(commands=['add'])
def add(message):
    user = bot.get_me()
    file = open('data/' + str(message.chat.id) + '.csv', 'a+')
    file.write("Hello,hello,hello\n")
    file.close()

    bot.send_message(message.chat.id, "What do you want to add?")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
	bot.reply_to(message, message.text)

bot.infinity_polling()