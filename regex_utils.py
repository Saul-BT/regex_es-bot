import re


def get_regex_well_fomatted(command_regex):
    re_command = r"\/(.*)\/([mixsua]*)"
    crafted_regex = None

    if re.search(re_command, command_regex):
        (regex, flags) = re.match(re_command, command_regex).groups()
        inline_flags = ''.join(map(lambda c: f'(?{c})', flags))
        crafted_regex = rf"{inline_flags}{regex}"

    return crafted_regex


def get_coincidences(command_regex, target_text):
    crafted_regex = get_regex_well_fomatted(command_regex)
    if crafted_regex:
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
        # Removing command, like /test
        command_regex = re.sub(r'^\/\w+\s+', '', update.message.text)
        coincidences = get_coincidences(command_regex, reply.text)
        if coincidences: message = '🟢'

    context.bot.send_message(chat_id, message, parse_mode='Markdown')


# Highlights all message matches
def search(update, context):
    chat_id = update.effective_chat.id
    reply = update.message.reply_to_message
    message = "🤨 Debe responder a un mensaje para utilizar este comando."

    if reply:
        command_regex = re.sub(r'^\/\w+\s+', '', update.message.text)
        matches = get_coincidences(command_regex, reply.text)
        message = "😔 No se encontraron coincidencias, pruebe a reformaular su regex."

        if matches:
            message = reply.text
            positions = [match.span() for match in matches]

            for position in positions[::-1]:
                (from_pos, to_pos) = position
                message = f"{message[:from_pos]}<b><u>{message[from_pos:to_pos]}</u></b>{message[to_pos:]}"

    context.bot.send_message(chat_id, message, parse_mode='HTML')


# Replaces all message matches
def replace(update, context):
    chat_id = update.effective_chat.id
    reply = update.message.reply_to_message
    message = "🤨 Debe responder a un mensaje para utilizar este comando."

    if reply:
        command_regex = re.sub(r'^\/\w+\s+', '', update.message.text)
        # Spliting by the whitespace character between regex and substitution
        [ command_regex, substitution ] = re.split(r'(?<=\/)\s+(?=\[.*\]$)', command_regex)
        crafted_regex = get_regex_well_fomatted(command_regex)
        message = "😔 No se encontraron coincidencias, pruebe a reformaular su regex."

        if crafted_regex:
            message = re.sub(crafted_regex, substitution[1:-1], reply.text)

    context.bot.send_message(chat_id, message, parse_mode='Markdown')
