import os
import requests
import re
import string_utils
import logger

IMGFLIP_USERNAME = os.getenv('IMGFLIP_USERNAME')
IMGFLIP_PASSWORD = os.getenv('IMGFLIP_PASSWORD')

MAKE_MEME_REQUEST_REGEX = "бот(,|(, | ))(го|сделай|давай|замути) (мем|мемас) " \
                          "(про|с) "


class UnknownSubjectError(Exception):
    """Error when finding meme subject (who to make meme about)"""
    pass


def is_make_meme_request(message):
    return string_utils.matches(message.text, MAKE_MEME_REQUEST_REGEX)


def handle_message(bot, message):
    try:
        url = generate_meme_url(message.text)
        bot.send_photo(message.chat.id, url)
    except UnknownSubjectError:
        s = "Не понял про кого мем..."
        bot.send_message(message.chat.id, s)
    except Exception as e:
        logger.log_chat_error(message, e)
        s = "Не понял что ты имеешь ввиду :( \nПереформулируй запрос плиз"
        bot.send_message(message.chat.id, s)


def generate_meme_url(text):
    result = requests.get("https://api.imgflip.com/get_memes")
    json_result = result.json()
    subject = string_utils.find_meme_subject(text)
    subject_index = __get_memesubject_index__(subject)
    if subject_index == -1:
        raise UnknownSubjectError()
    words = string_utils.find_texts_for_picture(text)
    template_id = json_result['data']['memes'][subject_index]['id']
    data = {
        'template_id': template_id,
        'username': IMGFLIP_USERNAME,
        'password': IMGFLIP_PASSWORD,
        'text0': words[0],
        'text1': words[1],
    }
    result = requests.post('https://api.imgflip.com/caption_image',
                           data=data).json()
    return result['data']['url']


def __get_memesubject_index__(subject):
    if re.match("дрейк(а|ом)", subject):
        return 0
    if re.match("кнопк(ами|и)", subject):
        return 1
    if re.match("парн(я|ем)", subject):
        return 2
    if re.match("человечк(а|ом)", subject):
        return 3
    if re.match("доге", subject):
        return 4
    if re.match("поворо(т|том)", subject):
        return 5
    if re.match("винни", subject):
        return 21
    if re.match("кнопкой", subject):
        return 22
    if re.match("пар[ау]", subject):
        return 24
    if re.match("картинк(ами|и)", subject):
        return 30
    if re.match("негр(а|ом)", subject):
        return 36
    if re.match("дикаприо", subject):
        return 58
    if re.match("кот(а|ом)", subject):
        return 63
    if re.match("спор", subject):
        return 85
    return -1
