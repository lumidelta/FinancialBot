import telebot
from telebot import types
from datetime import datetime
from pathlib import Path

with open("token.txt", "r") as f:
    token = f.read()
bot = telebot.TeleBot(token)


# 6 вывести за определенную дату
# 8 вывести за определенный период
# 9 вывести за месяц

# Wrapper for save file opening if not exist
def save_open(path, name, opts = 'r'):
    Path(path).mkdir(parents=True, exist_ok=True)
    try:
        # Hack for creating file
        new_opts = opts.replace('r+', 'a+').replace('r', 'a+')
        file = open(path + '/' + name, new_opts)
        # Rewind if asked to use r/r+ mod
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
    with open('help.txt', 'r') as f:
        s = ' '.join(f.readlines())
    bot.send_message(message.chat.id, s)

@bot.message_handler(commands=['newcat'])
def take_message(message): 
    splitted = message.text.split(' ', 1)
    try:
        # TODO: add check len(splitted) == 2
        newcat = splitted[1]
    except:
        # if input is just /newcat
        bot.send_message(message.chat.id, 'input "/newcat category" to add new category')
        return 
    # Open categories file for adding new category
    file = save_open('data', str(message.chat.id) + '_cat' + '.csv', 'a+')
    # We always use our categories in set, then they'll be sorted and exist only one instance
    catset = set([i.strip() for i in file.readlines()])
    catset.add(newcat)
    # Clear file
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
        # TODO: add check len(splitted) == 2
        badcat = splitted[1]
    except:
        # if input is just /delcat
        bot.send_message(message.chat.id, 'input "/delcat category" to delete category')
        return 
    # Open categories file for deleting category
    file = save_open('data', str(message.chat.id) + '_cat' + '.csv', 'r+')
    catset = set([i.strip() for i in file.readlines()])
    try:
        # Try to remove category if exist
        catset.remove(badcat)
    except:
        bot.send_message(message.chat.id, 'no such category')
        return
    # Clear file
    file.truncate(0) 
    file.seek(0)
    for cat in catset:
        file.write(cat + '\n')
    file.close()
    bot.send_message(message.chat.id, 'you delete category ' + badcat)
 
@bot.message_handler(commands=['cats'])
def show_cats(message):
    # TODO: add check len(splitted) == 1
    file = save_open('data', str(message.chat.id) + '_cat' + '.csv', 'r')
    catset = set([i.strip() for i in file.readlines()])
    file.close()
    if catset == set():
        bot.send_message(message.chat.id, 'there are no category :c ')
    else:
        cats = '\n'.join(catset)
        bot.send_message(message.chat.id, 'your cats: \n' + cats)

@bot.message_handler(commands=['excel'])
def excel(message):
    try:
        # Return full excel data
        with save_open('data', str(message.chat.id) + '.csv') as doc:
            bot.send_document(message.chat.id, doc)   
    except:
        bot.send_message(message.chat.id, 'there no records')  

@bot.message_handler(commands=['del'])
def del_last_record(message):
    try:
        with save_open('data', str(message.chat.id) + '.csv', 'r+') as file:
            # Delete last record
            newdata = file.readlines()[:-1]
            # Clear file
            file.seek(0)
            file.truncate(0)
            file.write(''.join(newdata))
        bot.send_message(message.chat.id, 'record was deleted')  
    except:
        bot.send_message(message.chat.id, 'you dont have any records')

# Turn on/off categories
@bot.message_handler(commands=['rotatecat'])
def rotate_cat(message):
    with save_open('data', str(message.chat.id) + '_set' + '.csv', 'a+') as file:
        file.seek(0)
        lines = file.readlines()
        # Check that file is not empty
        if (len(lines) != 0):
            # Rotate choise
            flag = 1 - int(lines[0])
            lines[0] = str(flag) + '\n'
            # Clear file
            file.seek(0)
            file.truncate(0)
            # Rewrite options
            file.write(''.join(lines))
        else:
            flag = 0
    if flag:
        bot.send_message(message.chat.id, 'categories on')  
    else:
        bot.send_message(message.chat.id, 'categories off') 

@bot.message_handler(content_types=['text'])
def take_message(message): 
    splitted = message.text.split(' ', 1)
    if len(splitted) != 2:
        bot.send_message(message.chat.id, 'input "cost name" with space')
        return 

    # Open file for categories and settings
    file = save_open('data', str(message.chat.id) + '_cat' + '.csv', 'r')
    file_set = save_open('data', str(message.chat.id) + '_set' + '.csv', 'a+')
    file_set.seek(0)
    lines = file_set.readlines()
    # Check that settings file is correct
    if (len(lines) == 2):
        flag = int(lines[0])
        record_flag = int(lines[1])
    else:
        # Create file with default settings
        file_set.write("0\n0\n0\n")
        flag = 0
        record_flag = 0
    catset = set(file.readlines())
    file.close()
    
    # Check that Adding Category is available
    if record_flag == 1:
        # TODO: WTF?
        file = save_open('data', str(message.chat.id) + '.csv', 'a+')
        file.write('\n')
        file.close()
        file_set = save_open('data', str(message.chat.id) + '_set' + '.csv', 'a+')
        file_set.seek(0)
        lines = file_set.readlines()
        bot.edit_message_text(chat_id=message.chat.id, message_id=int(lines[2]), text='done')
        file_set.close()
        
    # Check that categories is enabled
    if flag == 1:
        # Write new data
        file = save_open('data', str(message.chat.id) + '.csv', 'a+')
        file.write(str(datetime.now()) + ', ' + ', '.join(splitted) + ', ')
        file.close()
        # Add buttons
        mainmenu = types.InlineKeyboardMarkup()
        buttons = []
        for i in catset:
            buttons.append(types.InlineKeyboardButton(text=i, callback_data=i))
            mainmenu.add(buttons[-1])
        if len(catset) != 0:    
            bot.send_message(message.chat.id, 'choose category', reply_markup=mainmenu)
        # Edit settings
        file = save_open('data', str(message.chat.id) + '_set' + '.csv', 'a+')
        file.seek(0)
        lines = file.readlines()
        # Add pending edit of message flags
        lines[1] = '1\n'
        lines[2] = str(message.message_id + 1) + '\n'
        file.seek(0)
        file.truncate(0)
        file.write(''.join(lines))
        file.close()
    else:
        # Just write new data
        file = save_open('data', str(message.chat.id) + '.csv', 'a+')
        file.write(str(datetime.now()) + ', ' + ', '.join(splitted) + ', \n')
        file.close()
        bot.send_message(message.chat.id, 'done')
    

# Handler for editing category-choose message
@bot.callback_query_handler(lambda query: True)
def catbuttons(query):
    file = save_open('data', str(query.message.chat.id) + '_cat' + '.csv', 'r')
    catset = set(file.readlines())
    file.close()
    for cat in catset:
        if query.data == cat:
            file = save_open('data', str(query.message.chat.id) + '.csv', 'a+')
            # Add category to the end of the file
            file.write(cat.strip() + '\n')
            file.close()
            flag = 0
            break
    with save_open('data', str(query.message.chat.id) + '_set' + '.csv', 'r') as file:
        # Remove pending edit of message flag
        lines = file.readlines()
        lines[1] = '0\n'
        lines[2] = '0\n'
    with save_open('data', str(query.message.chat.id) + '_set' + '.csv', 'w') as file:
        file.write(''.join(lines)) 
    
    bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, text='done')


bot.infinity_polling()