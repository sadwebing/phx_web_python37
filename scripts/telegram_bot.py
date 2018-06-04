#!/usr/bin/env python
#-_- coding:utf-8 -_-
#author: Arno
#update: 2018/06/04  telegram_bot

import os, sys, datetime, logging
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "phxweb.settings")

from phxweb         import settings
from telegram.ext   import Updater, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler, Handler
from telegram       import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton
from monitor.models import telegram_user_id_t

logging.basicConfig(level=logging.INFO, filename="bot.log", format='%(asctime)s - %(levelname)s - %(message)s')

user_id_l = {}
s = telegram_user_id_t.objects.all()
for i in s:
    user_id_l[i.user] = {}
    user_id_l[i.user]['name']    = i.name
    user_id_l[i.user]['user_id'] = i.user_id

def start(bot, update):
    #bot.sendMessage(chat_id=settings.TELEGRAM_API['chat_id']['arno_test'], text="I'm a bot, please talk to me!")
    #update.message.reply_text("Welcome to my awesome bot!")
    reply_keyboard = [['option1', 'option2', 'option3', 'exit']]
    #print dir(update.message.reply_markdown)
    update.message.reply_text("开始选择",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard)
    )
    return 'option'

def at(bot, update, args):
    text = ""
    if settings.TELEGRAM_API['user_group'].has_key(args[0]):
        for user in settings.TELEGRAM_API['user_group'][args[0]]:
            text += "[%s](tg://user?id=%s) " %(user_id_l[user]['name'], user_id_l[user]['user_id']) if user_id_l.has_key(user) else ""

    text += '\r\n' + " ".join(args[1:]) if len(args) > 1 else ""

    bot.send_message(chat_id=update.message.chat_id, text=text, parse_mode='Markdown')

def start_bot():
    my_bot = Updater(settings.TELEGRAM_API['api']['sa_monitor_bot'])

    dp = my_bot.dispatcher

    #dp.add_handler(CommandHandler("start", start))

    dp.add_handler(CommandHandler("at", at, pass_args=True))

    my_bot.start_polling()
    my_bot.idle()

if __name__ == "__main__":
    start_bot()