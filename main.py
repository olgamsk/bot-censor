import telebot
import re
import os.path

bot = telebot.TeleBot('5876209096:AAHYH3sKWCik5CQy9P3q97l6OKidb6K5TYI')

baza = {}

@bot.message_handler(commands=['add'])
def add_word(message):
    chat_id = message.chat.id
    this_chat_member = bot.get_chat_member(message.chat.id, message.from_user.id)
    filename = 'words_' + str(chat_id) + '.txt'
    if this_chat_member.status == "administrator" or this_chat_member.status == 'creator':
        if os.path.exists(filename):
            open_file = open(filename, 'a')
        else:
            open_file = open(filename, 'w')
        censoring_words = message.text[5:].lower()
        if censoring_words != '':
            open_file.write(censoring_words + '\n')
            open_file.close()
            bot.reply_to(message, "Добавлено!")
        else:
            bot.reply_to(message, "Нельзя добавить пустоту.")
    else:
        bot.reply_to(message, "Только администраторы группы могут поддерживать цензурный аппарат.")

@bot.message_handler(commands=['remove'])
def remove_word(message):
    chat_id = message.chat.id
    filename = 'words_' + str(chat_id) + '.txt'
    this_chat_member = bot.get_chat_member(message.chat.id, message.from_user.id)
    list_words = []
    if this_chat_member.status == "administrator" or this_chat_member.status == 'creator':
        if os.path.exists(filename):
            censoring_word = message.text[8:].lower()
            if censoring_word != '':
                open_file = open(filename, 'r')
                for x in open_file:
                    list_words.append(x.replace('\n', ''))
                for x in list_words:
                    if x == censoring_word:
                        list_words.remove(x)
                open_file.close()
                open_file = open(filename, 'w')
                for x in list_words:
                    open_file.write(x + '\n')
                open_file.close()
                bot.reply_to(message, 'Удалено.')
            else:
                bot.reply_to(message, 'Нельзя удалить пустоту.')
        else:
            bot.reply_to(message, 'В вашем чате нет запрещённых слов.')
    else:
        bot.reply_to(message, "Только администраторы группы могут поддерживать цензурный аппарат.")

@bot.message_handler(commands=['list'])
def list_of_words(message):
    chat_id = message.chat.id
    filename = 'words_' + str(chat_id) + '.txt'
    this_chat_member = bot.get_chat_member(message.chat.id, message.from_user.id)
    if this_chat_member.status == "administrator" or this_chat_member.status == 'creator':
        if os.path.exists(filename):
            open_file = open(filename, 'r')
            list_words = ''
            for x in open_file:
                list_words = list_words + x
            if list_words == '':
                bot.reply_to(message, 'В вашем чате нет запрещённых слов.')
            else:
                bot.reply_to(message, list_words)
            open_file.close()
        else:
            bot.reply_to(message, 'В вашем чате нет запрещённых слов.')
    else:
        bot.reply_to(message, "Только администраторы группы могут поддерживать цензурный аппарат.")

@bot.message_handler(content_types=['text'])
def text_handler(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    if baza.get(user_id) == None:
        baza[user_id] = 0
    filename = 'words_' + str(chat_id) + '.txt'
    if os.path.exists(filename):
        open_file = open(filename, 'r')
        for x in open_file:
            if re.search(x.strip(), message.text.lower()):
                baza[user_id] += 1
                bot.delete_message(chat_id, message.id, timeout=None)
                break
        open_file.close()
    if baza[user_id] == 4:
        bot.kick_chat_member(chat_id, user_id)

bot.polling()