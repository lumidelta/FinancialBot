import telebot
from telebot import types
from datetime import datetime
with open("token.txt", "r") as f:
    token = f.read()
bot = telebot.TeleBot(token)

# 1 добавление категории + 
# 2 выбор категории с помощью кнопок 
# 3 возможность отключить категорию
# 4 категории не повторялись +
# 5 переделать запись 
# 6 вывести за определенную дату
# 7 удаление категорий + 
# 8 вывести за определенный период
# 9 вывести за месяц

   # mainmenu = types.InlineKeyboardMarkup()
    # key1 = types.InlineKeyboardButton(text='about', callback_data='key1')
    # key2 = types.InlineKeyboardButton(text='new record', callback_data='key2')
    # key2 = types.InlineKeyboardButton(text='new category', callback_data='key3')
    # mainmenu.add(key1, key2)
    #bot.send_message(message.chat.id, 'choose category', reply_markup=mainmenu)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, '\help ..... \\newcat .... \excel ...')

@bot.message_handler(commands=['help'])
def help(message):
	bot.send_message(message.chat.id, ' smt useful ')

@bot.message_handler(commands=['newcat'])
def take_message(message): 
    splitted = message.text.split(' ', 1)
    try:
        newcat = splitted[1]
    except:
        bot.send_message(message.chat.id, 'input "/newcat category" to add new category')
        return 
    file = open('data/' + str(message.chat.id) + '_cat' + '.csv', 'r+')
    catset = set([i.strip() for i in file.readlines()])
    catset.add(newcat)
    file.truncate(0) 
    file.seek(0)
    for cat in catset:
        file.write(cat + '\n')
    file.close()   
    bot.send_message(message.chat.id, 'you add new category ' + cat)

@bot.message_handler(commands=['delcat'])
def take_message(message): 
    splitted = message.text.split(' ', 1)
    try:
        badcat = splitted[1]
    except:
        bot.send_message(message.chat.id, 'input "/delcat category" to delete category')
        return 
    file = open('data/' + str(message.chat.id) + '_cat' + '.csv', 'r+')
    catset = set([i.strip() for i in file.readlines()])
    try:
        catset.remove(badcat)
    except:
        bot.send_message(message.chat.id, 'no such category')
        return
    file.truncate(0) 
    file.seek(0)
    for cat in catset:
        file.write(cat + '\n')
    file.close()
    bot.send_message(message.chat.id, 'you delete category ' + badcat)
 
 
    

@bot.message_handler(commands=['excel'])
def excel(message):
    with open('./data/' + str(message.chat.id) + '.csv') as doc:
	    bot.send_document(message.chat.id, doc)   

@bot.message_handler(content_types=['text'])
def take_message(message): 
    splitted = message.text.split(' ', 1)
    try:
        int(splitted[0])
    except:
        bot.send_message(message.chat.id, 'input "cost name" with space')
        
    if len(splitted) != 2:
        bot.send_message(message.chat.id, 'input "cost name" with space')
        return 


    file = open('data/' + str(message.chat.id) + '.csv', 'a+')
    file.write(str(datetime.now()) + ', ' + ', '.join(splitted) + "\n")
    file.close()


# @bot.callback_query_handler(lambda query: query.data == "key2")
# def send_welcome(query):
#     bot.send_message(query.message.chat.id, 'type new category')

# @bot.callback_query_handler(lambda query: query.data == "key3")
# def send_welcome(query):
#     bot.send_message(query.message.chat.id, 'here is your data')

# @bot.callback_query_handler(lambda query: query.data == "key4")
# def send_welcome(query):
#     bot.send_message(query.message.chat.id, 'about')

# @bot.callback_query_handler(lambda query: query.data == "key1")
# def send_welcome(query):
#     add(query.message)

# @bot.message_handler(func=lambda message: True)
# def echo_all(message):
# 	bot.reply_to(message, message.text)

bot.infinity_polling()