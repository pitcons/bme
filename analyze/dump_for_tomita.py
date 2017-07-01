# encoding: utf-8
import os
import re

import db
from config import config

REPLACE_MAP = {
    'HTML_I_OPEN': '',
    'HTML_I_CLOSE': '',
    '[': 'SQUARE_BRACKET_OPEN',
    ']': 'SQUARE_BRACKET_CLOSE',
}

def dump_for_tomita():

    path = os.path.join(config.data_path, 'for_tomita.txt')
    with open(path, 'w') as f:
        n = 0
        for article in db.Article.objects.all():
            text = article.first_sentence
            # text = re.sub(r'<([a-zA-Z]*)>', lambda m: ' HTML_' + m.group(1).upper() + '_OPEN ', text)
            # text = re.sub(r'</([a-zA-Z]*)>', lambda m: ' HTML_' + m.group(1).upper() + '_CLOSE ', text)
            # for key, value in REPLACE_MAP.items():
            #     text = text.replace(key, value)

            f.write(text)
            f.write('\n')

            n += 1
            if n % 10 == 0:
                print(n)
