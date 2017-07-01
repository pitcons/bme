# encoding: utf-8
import os
import re
import html
import lxml.html
from lxml import etree

import db
from config import config
from tools.parsing import body_as_etree

SPACES_RE = re.compile(r'[\s\n]+')


def build_first_sentences():
    """Создание html с несколькими первыми предложениями в статьях
    """
    path = os.path.join(config.data_path, 'first_sentences.html')
    with open(path, 'w') as f:
        for article in db.Article.objects.all()[:100]:
            body = body_as_etree(article.raw)
            content = body.xpath("//div[@id='mw-content-text']")[0]
            fist_p = etree.tostring(content.xpath('//p')[0])
            text = html.unescape(fist_p.decode('utf-8'))
            f.write(text)
            article.first_sentence = text
            article.save()
