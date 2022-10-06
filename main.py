import telebot
from telebot import types
from datetime import datetime
from pathlib import Path

with open("token.txt", "r") as f:
    token = f.read()
bot = telebot.TeleBot(token)

# 2 выбор категории с помощью кнопок 
# 3 возможность отключить категорию
# 5 переделать запись + 
# 6 вывести за определенную дату
# 8 вывести за определенный период
# 9 вывести за месяц
# 10 отдельное сообщение при количестве категорий 0 для take_message
# 11 /excel при первом запуске все ломает
# mainmenu = types.InlineKeyboardMarkup()
# key1 = types.InlineKeyboardButton(text='about', callback_data='key1')
# key2 = types.InlineKeyboardButton(text='new record', callback_data='key2')
# key2 = types.InlineKeyboardButton(text='new category', callback_data='key3')
# mainmenu.add(key1, key2)
#bot.send_message(message.chat.id, 'choose category', reply_markup=mainmenu)

def save_open(path, name, opts = 'r'):
    Path(path).mkdir(parents=True, exist_ok=True)
    try:
        new_opts = opts.replace('r+', 'a+').replace('r', 'a+')
        file = open(path + '/' + name, new_opts)
        if opts == 'r+' or opts == 'r':
            file.seek(0)
        return file
    except:
        raise RuntimeError("Error with opening file")


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, '\\help ..... \\newcat .... \\excel ...')

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
    file = save_open('data', str(message.chat.id) + '_cat' + '.csv', 'a+')
    catset = set([i.strip() for i in file.readlines()])
    catset.add(newcat)
    file.truncate(0) 
    file.seek(0)
    for cat in catset:
        file.write(cat + '\n')
    file.close()   
    bot.send_message(message.chat.id, 'you add new category ' + newcat)

@bot.message_handler(commands=['delcat'])
def take_message(message): 
    splitted = message.text.split(' ', 1)
    try:
        badcat = splitted[1]
    except:
        bot.send_message(message.chat.id, 'input "/delcat category" to delete category')
        return 
    file = save_open('data', str(message.chat.id) + '_cat' + '.csv', 'r+')
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
 
@bot.message_handler(commands=['cats'])
def show_cats(message): 
    file = save_open('data', str(message.chat.id) + '_cat' + '.csv', 'r')
    catset = set([i.strip() for i in file.readlines()])
    file.close()
    if catset == set():
        bot.send_message(message.chat.id, 'there are no category :c ')
    else:
        cats = '\n'.join(catset)
        bot.send_message(message.chat.id, 'so many cats \n' + cats)
    

@bot.message_handler(commands=['excel'])
def excel(message):
    with save_open('data', str(message.chat.id) + '.csv') as doc:
	    bot.send_document(message.chat.id, doc)   

@bot.message_handler(commands=['del'])
def del_last_record(message):
    try:
        with save_open('data', str(message.chat.id) + '.csv', 'r+') as file:
            newdata = file.readlines()[:-1]
            file.seek(0)
            file.truncate(0)
            file.write(''.join(newdata))
        bot.send_message(message.chat.id, 'record was deleted')  
    except:
        bot.send_message(message.chat.id, 'you dont have any records')

@bot.message_handler(commands=['rotatecat'])
def rotate_cat(message):
    with save_open('data', str(message.chat.id) + '_set' + '.csv', 'a+') as file:
        file.seek(0)
        lines = file.readlines()
        try:
            flag = int(lines[0])
            if flag == 1:
                flag = 0
                lines[0] = '0\n'
            else:
                flag = 1
                lines[0] = '1\n'
            file.seek(0)
            file.truncate(0)
            file.write(''.join(lines))
        except:
            flag = 0
    if flag:
        bot.send_message(message.chat.id, 'categories on')  
    else:
        bot.send_message(message.chat.id, 'categories off') 

@bot.message_handler(content_types=['text'])
def take_message(message): 
    splitted = message.text.split(' ', 1)
    try:
        int(splitted[0])
    except:
        bot.send_message(message.chat.id, 'input "cost name" with space')
        return   
    if len(splitted) != 2:
        bot.send_message(message.chat.id, 'input "cost name" with space')
        return 

    file = save_open('data', str(message.chat.id) + '_cat' + '.csv', 'r')
    file_set = save_open('data', str(message.chat.id) + '_set' + '.csv', 'a+')
    file_set.seek(0)
    lines = file_set.readlines()
    try:
        flag = int(lines[0])
        record_flag = int(lines[1])
    except:
        file_set.write("0\n0\n0\n")
        flag = 0
        record_flag = 0
    catset = set(file.readlines())
    file.close()
    
    if record_flag == 1:
        file = save_open('data', str(message.chat.id) + '.csv', 'a+')
        file.write('\n')
        file.close()
        file_set = save_open('data', str(message.chat.id) + '_set' + '.csv', 'a+')
        file_set.seek(0)
        lines = file_set.readlines()
        bot.edit_message_text(chat_id=message.chat.id, message_id=int(lines[2]), text='done')
        file_set.close()
        
    if flag == 1:
        file = save_open('data', str(message.chat.id) + '.csv', 'a+')
        file.write(str(datetime.now()) + ', ' + ', '.join(splitted) + ', ')
        file.close()
        mainmenu = types.InlineKeyboardMarkup()
        buttons = []
        for i in catset:
            buttons.append(types.InlineKeyboardButton(text=i, callback_data=i))
            mainmenu.add(buttons[-1])
        bot.send_message(message.chat.id, 'choose category', reply_markup=mainmenu)
        file = save_open('data', str(message.chat.id) + '_set' + '.csv', 'a+')
        file.seek(0)
        lines = file.readlines()
        lines[1] = '1\n'
        lines[2] = str(message.message_id + 1) + '\n'
        file.seek(0)
        file.truncate(0)
        file.write(''.join(lines))
        file.close()
    else:
        file = save_open('data', str(message.chat.id) + '.csv', 'a+')
        file.write(str(datetime.now()) + ', ' + ', '.join(splitted) + ', \n')
        file.close()
        bot.send_message(message.chat.id, 'done')
    

@bot.callback_query_handler(lambda query: True)
def catbuttons(query):
    file = save_open('data', str(query.message.chat.id) + '_cat' + '.csv', 'r')
    catset = set(file.readlines())
    file.close()
    for cat in catset:
        if query.data == cat:
            file = save_open('data', str(query.message.chat.id) + '.csv', 'a+')
            file.write(cat.strip() + '\n')
            file.close()
            flag = 0
            break
    with save_open('data', str(query.message.chat.id) + '_set' + '.csv', 'r') as file:
        lines = file.readlines()
        lines[1] = '0\n'
        lines[2] = '0\n'
    with save_open('data', str(query.message.chat.id) + '_set' + '.csv', 'w') as file:
        file.write(''.join(lines)) 
    
    bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, text='done')

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