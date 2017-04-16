
import re
import os
import types
import html
from owlready import Thing, ANNOTATIONS
from lxml import etree

import db
from config import config
from tools.parsing import body_as_etree

TOME_RE = re.compile(r'Категория:Том (?P<number>[0-9]+)')
TAG_RE = re.compile(r'<[^>]+>')


def remove_tags(text):
    return TAG_RE.sub('', text)


class Bme3Analyze:

    def __init__(self):
        self.tomes = {}

    def setup_tome(self, article, root):
        """Определение тома
        """
        path = root.xpath('//div[@id="mw-normal-catlinks"]//a')

        if not path:
            raise ValueError("Can't setup tome {}".format(article.url))

        for item in path:
            title = item.get('title', '')
            m = TOME_RE.match(title)
            if m:
                article.tome = int(m['number'])
                article.save()
            elif title.startswith('Служебная'):
                pass
            else:
                raise ValueError("Can't setup tome {}".format(article.url))

    def extract_content(self, db_article, article, root):
        """Извлечение содержания статьи
        """
        content = root.xpath('//div[@id="mw-content-text"]')[0]
        text = etree.tostring(content).decode('utf-8')
        ANNOTATIONS[article].add_annotation(
            "comment", html.unescape(remove_tags(text)))
        ANNOTATIONS[article].add_annotation(
            "source", db_article.url)


    def process_article(self, article):
        root = body_as_etree(article.raw)
        # Определяем том
        self.setup_tome(article, root)
        # Выделяем содержание
        # self.extract_content(db_article, article, root)

    def run(self):
        # self.ensure_tomes()
        for db_article in db.Article.objects[:1000]:
            if not TOME_RE.match(db_article.title):
                self.process_article(db_article)


def bme3analyze():
    Bme3Analyze().run()
