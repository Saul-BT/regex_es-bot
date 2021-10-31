import os
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from captcha import create_captcha, process_message 
from regex_utils import test, search, replace


def welcome(update, context):
    chat_id = update.effective_chat.id
    new_member_ids = [member.id for member in update.message.new_chat_members]
    
    if context.bot.id not in new_member_ids:
        context.bot.send_message(chat_id, 'Bienvenido puto')
        create_captcha(update, context, chat_id, new_member_ids[0])
    

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

updater = Updater(os.environ['BOT_TOKEN'], use_context=True)
dispatcher = updater.dispatcher

# Command Handlers
dispatcher.add_handler(CommandHandler('test', test))
dispatcher.add_handler(CommandHandler('search', search))
dispatcher.add_handler(CommandHandler('replace', replace))

# Message Handlers
dispatcher.add_handler(MessageHandler(Filters.status_update.new_chat_members, welcome))
message_handler = MessageHandler(Filters.text, process_message, pass_user_data=True)
dispatcher.add_handler(message_handler)

updater.start_polling()
updater.idle()
