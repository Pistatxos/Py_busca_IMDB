#!/usr/local/bin/python
# -*- coding: UTF-8 -*-

from telegram import *
from telegram.ext import *
from datetime import datetime
from buscar_pelis_IMDB import buscar_imdb

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

## Añade tu token
TOKEN = ''

updater = Updater(TOKEN)
dispatcher = updater.dispatcher

start = '''Bienvenido/da:\nPara buscar una peli/serie hay que escribir "*Buscar y el nombre de la película o serie".\nEjemplo: *Buscar titanic'''

def startCommand(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,text=start)

def messageHandler(update: Update, context: CallbackContext):
    try:
        text = update.message.text
        if '*Buscar ' in text:
            busqueda = buscar_peli(text.replace('*Buscar','').strip())
            context.bot.send_message(chat_id=update.effective_chat.id,text=busqueda)
        
    except Exception as error:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=f"- Error: {error}-\nPor favor, vuelve a intentarlo, sino contacta con el administrador reenviando este mensaje de error.")


def queryHandler(update: Update, context: CallbackContext):
    query = update.callback_query.data
    update.callback_query.answer()

dispatcher.add_handler(CommandHandler("start", startCommand))
dispatcher.add_handler(MessageHandler(Filters.text, messageHandler))
dispatcher.add_handler(CallbackQueryHandler(queryHandler))

updater.start_polling()
