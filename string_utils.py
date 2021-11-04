import re


def matches(message, options):
    if type(options) == str:
        return re.match(options, message)
    for s in options:
        if re.match(s, message.lower()):
            return True
    return False


def word_before(text, delimiter):
    split = list(filter(lambda m: m, text.split(delimiter)[0].split(" ")))
    return split[-1]


def find_meme_subject(text):
    if len(text.split('мемас')) > 1:
        # Text contains 'мемас', trying to find subject here
        if "мемас" not in text.split(":")[0]:
            # Text contains 'мемас', but it is after ":", don't know how to
            # parse it
            raise Exception
    else:
        # No word 'мемас', trying to find word 'мем'
        if "мем" not in text.split(":")[0]:
            # Text contains 'мем', but it is after ":", don't know how to
            # parse it
            raise Exception
    subject = word_before(text, ":")
    return subject.strip()


def find_texts_for_picture(text):
    result = map(str.strip, text.split(':')[1].split(','))
    return list(e for e in result if e)
