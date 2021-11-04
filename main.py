import os
import dotenv
import telebot

dotenv.load_dotenv()

import mememaker

API_KEY = os.getenv('API_KEY')
bot = telebot.TeleBot(API_KEY)


@bot.message_handler(func=mememaker.is_make_meme_request)
def mememaker_handle_message(message):
    mememaker.handle_message(bot, message)


bot.infinity_polling()
