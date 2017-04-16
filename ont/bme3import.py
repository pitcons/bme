
import re
import os
import types
import html
from owlready import Thing, ANNOTATIONS
from lxml import etree

import db
from config import config
from tools.parsing import body_as_etree
from tools.ontology import correct_owl_id
from .onto import Article, Tome, onto

TOME_RE = re.compile(r'Категория:Том (?P<number>[0-9]+)')
TAG_RE = re.compile(r'<[^>]+>')


def remove_tags(text):
    return TAG_RE.sub('', text)


class Bme3Import:

    def __init__(self):
        self.tomes = {}

    def ensure_tomes(self):
        for number in range(1, 29):
            class_id = 'Tome_{0:02d}'.format(number)
            self.tomes[number] = types.new_class(
                correct_owl_id(class_id),
                (Tome, ),
                kwds = { "ontology" : onto }
            )

    def extract_tome(self, db_article, article, root):
        """Определение тома
        """
        path = root.xpath('//div[@id="mw-normal-catlinks"]//a')

        if not path:
            raise ValueError("Can't import {}".format(db_article.url))

        for item in path:
            title = item.get('title', '')
            m = TOME_RE.match(title)
            if m:
                tome = self.tomes[int(m['number'])]
                article.is_a.append(tome)
            elif title.startswith('Служебная'):
                pass
            else:
                print(title)
                print()
                raise ValueError("Can't determine tome")

    def extract_content(self, db_article, article, root):
        """Извлечение содержания статьи
        """
        content = root.xpath('//div[@id="mw-content-text"]')[0]
        text = etree.tostring(content).decode('utf-8')
        ANNOTATIONS[article].add_annotation(
            "comment", html.unescape(remove_tags(text)))
        ANNOTATIONS[article].add_annotation(
            "source", db_article.url)


    def process_article(self, db_article):
        article = Article(
            correct_owl_id(db_article.title),
            title=db_article.title
        )
        root = body_as_etree(db_article.raw)
        # Определяем том
        self.extract_tome(db_article, article, root)
        # Выделяем содержание
        self.extract_content(db_article, article, root)

    def run(self):
        self.ensure_tomes()
        for db_article in db.Article.objects[:1000]:
            if not TOME_RE.match(db_article.title):
                self.process_article(db_article)


def bme3import():
    Bme3Import().run()
    onto.save()
