import re


RE_COMMAND = r'^\/\w+\s+'
RE_REGEX = r'^\/(?P<regex>(?:[^\/]|\\\/)*)\/(?P<flags>[gmixsua]*)$'
RE_REGEXSUB = r'^s\/(?P<regex>(?:[^\/]|\\\/)*)\/(?P<substitution>[^\/]*)\/(?P<flags>[gmixsua]*)$'



def get_regex_with_flags(regex, flags):
    count = 1

    if 'g' in flags:
        count = 0
        flags = flags.replace('g', '')

    if flags:
        return rf'(?{flags}){regex}', count
    else:
        return regex, count



def get_regex_well_fomatted(command_regex):
    crafted_regex = None
    m = re.match(RE_REGEX, command_regex)

    if m:
        crafted_regex, count = get_regex_with_flags(
            m.group('regex'), m.group('flags'))

    return crafted_regex, count


def get_coincidences(command_regex, target_text):
    crafted_regex, _ = get_regex_well_fomatted(command_regex)
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
        command_regex = re.sub(RE_COMMAND, '', update.message.text)
        coincidences = get_coincidences(command_regex, reply.text)
        if coincidences: message = '🟢'

    context.bot.send_message(chat_id, message, parse_mode='Markdown')


# Highlights all message matches
def search(update, context):
    chat_id = update.effective_chat.id
    reply = update.message.reply_to_message
    message = "🤨 Debe responder a un mensaje para utilizar este comando."

    if reply:
        command_regex = re.sub(RE_COMMAND, '', update.message.text)
        matches = get_coincidences(command_regex, reply.text)
        message = "😔 No se encontraron coincidencias, pruebe a reformular su regex."

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
        command_regex = re.sub(RE_COMMAND, '', update.message.text)
        # Spliting by the whitespace character between regex and substitution
        [ command_regex, substitution ] = re.split(r'(?<=\/[mixsua]*)\s+(?=\[.*\]$)', command_regex)
        crafted_regex, count = get_regex_well_fomatted(command_regex)
        message = "😔 No se encontraron coincidencias, pruebe a reformaular su regex."

        if crafted_regex:
            message = re.sub(crafted_regex, substitution[1:-1], reply.text, count)

    context.bot.send_message(chat_id, message, parse_mode='Markdown')




def exec_replace(matches, text) -> str:
    regex = matches.group('regex')
    substitution = matches.group('substitution')
    flags = matches.group('flags')
    crafted_regex, count = get_regex_with_flags(regex, flags)

    return re.sub(crafted_regex, substitution, text, count)