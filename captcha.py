import re
import random
import threading

from regex_utils import RE_REGEXSUB, exec_replace

CAPTCHAS = {}
REGEXES = [
    r'[rR]eg[eE]xp?( is love)?',
    r'tarod es .*',
    r'Stay (at home|safe)',
    r'Me [^\s]+ los gatos',
    r'Te voy a mandar al hos(pi)?tal',
    r'Comete el (pas|man)tel encima del (pas|man)tel',
    r'Acaricia al [gp]ato',
    
]


# TODO: Integrate this with user welcome
# Set a countdown for the user to validate the captcha
def print_growing_penis(context, chat_id, text, message_id = None):
    message = None

    if not message_id:
        message = context.bot.send_message(chat_id, text+'D', parse_mode='Markdown')
    else:
        message = context.bot.edit_message_text(chat_id=chat_id, text=text+'D', message_id=message_id)

    threading.Timer(
        5.0,
        lambda : print_growing_penis(context, chat_id, text+'=', message.message_id)
    ).start()


# Checks if the user message matches the captcha regex
def check(reCaptcha, string):
    match = re.match(reCaptcha, string)

    return match != None



def create_captcha(update, context, chat_id, user_id):
    if not chat_id in CAPTCHAS:
        CAPTCHAS[chat_id] = {}

    if not user_id in CAPTCHAS[chat_id]:
        print_growing_penis(context, chat_id, "3=")
        CAPTCHAS[chat_id][user_id] = get_rand_captcha(update, context)



def get_rand_captcha(update, context):
    regex = random.choice(REGEXES)
    chat_id = update.effective_chat.id
    message_id = update.message.message_id
    message = f"Cadena que coincida con `/{regex}/` (case sentive): "

    context.bot.send_message(chat_id, message, parse_mode='Markdown', reply_to_message_id=message_id)

    return regex



def get_user_captcha(user_id, chat_id):
    if chat_id in CAPTCHAS:
        if user_id in CAPTCHAS[chat_id]:
            return CAPTCHAS[chat_id][user_id]



def process_message(update, context):
    chat_id = update.effective_chat.id
    reply = update.message.reply_to_message
    user_id = update.message.from_user.id
    message_id = update.message.message_id
    user_captcha = get_user_captcha(user_id, chat_id)

    if user_captcha:
        message = '🔴 Mal, prueba de nuevo.'

        if check(user_captcha, update.message.text):
            message = '🟢 Bieeeen :D'
            del CAPTCHAS[chat_id][user_id]
    
        context.bot.send_message(
            chat_id, message,
            parse_mode='Markdown',
            reply_to_message_id=message_id
        )

    else:
        m = re.match(RE_REGEXSUB, update.message.text)

        if m and reply:
            message = exec_replace(m, reply.text)
            context.bot.send_message(chat_id, message, parse_mode='Markdown')