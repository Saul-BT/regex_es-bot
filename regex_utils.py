import re



def get_coincidences(command_text, target_text):
    re_command = r"\/\w+\s+\/(.*)\/([mixsua]*)"

    if re.search(re_command, command_text):
        (regex, flags) = re.match(re_command, command_text).groups()
        inline_flags = ''.join(map(lambda c: f'(?{c})', flags))
        crafted_regex = rf"{inline_flags}{regex}"
        match = re.search(crafted_regex, target_text)

        if match:
            pattern = re.compile(crafted_regex)
            return re.finditer(pattern, target_text)


# Checks if a message matches the user regex
def test(update, context):
    chat_id = update.effective_chat.id
    reply = update.message.reply_to_message
    message = "🤨 Debe responder a un mensaje para utilizar este comando."

    if reply:
        message = '🔴'
        coincidences = get_coincidences(update.message.text, reply.text)
        if coincidences: message = '🟢'

    context.bot.send_message(chat_id, message, parse_mode='Markdown')


# Highlights all message matches
def search(update, context):
    chat_id = update.effective_chat.id
    reply = update.message.reply_to_message
    message = "🤨 Debe responder a un mensaje para utilizar este comando."

    if reply:
        matches = get_coincidences(update.message.text, reply.text)
        message = "😔 No se encontraron coincidencias, pruebe a reformaular su regex."

        if matches:
            message = reply.text
            positions = [match.span() for match in matches]

            for position in positions[::-1]:
                (from_pos, to_pos) = position
                message = f"{message[:from_pos]}<b><u>{message[from_pos:to_pos]}</u></b>{message[to_pos:]}"

    context.bot.send_message(chat_id, message, parse_mode='HTML')
