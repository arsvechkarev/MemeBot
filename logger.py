
def log_chat_error(message, e: Exception):
    print(
        'Exception in chat (' + str(message.chat) + ', '
        + str(message.chat.id) + '): ' + str(e)
    )
