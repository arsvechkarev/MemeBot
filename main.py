import os
import telebot
import requests

from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')
IMGFLIP_USERNAME = os.getenv('IMGFLIP_USERNAME')
IMGFLIP_PASSWORD = os.getenv('IMGFLIP_PASSWORD')

bot = telebot.TeleBot(API_KEY)


@bot.message_handler(regexp=("((Б|б)от(, | )го (мем|мемас)|"
                             "(Б|б)от, мем)")
                     )
def handle_message(message):
    try:
        bot.send_photo(message.chat.id, get_random_meme(message.text))
    except Exception as e:
        print("Error:" + str(e))
        pass


def get_random_meme(message):
    result = requests.get("https://api.imgflip.com/get_memes")
    json = result.json()
    words = message.split(':')[1].split(',')
    template_id = json['data']['memes'][8]['id']
    result = requests.post('https://api.imgflip.com/caption_image', data={
        'template_id': template_id,
        'username': IMGFLIP_USERNAME,
        'password': IMGFLIP_PASSWORD,
        'text0': words[0],
        'text1': words[1],
    }).json()
    print(result)
    return result['data']['url']


bot.infinity_polling()
