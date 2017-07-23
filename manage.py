# encoding: utf-8
import os
import atexit
import asyncio

import fire
import mongoengine
from aiocache import RedisCache

import db
from config import config
from crawlers.bme3load import bme3load

from analyze.build_first_sentences import build_first_sentences
from analyze.rutez_paths import rutez_paths
from analyze.extract_persons import extract_persons
from analyze.extract_links import extract_links
from analyze.dump_for_tomita import dump_for_tomita
from analyze.fill_norm_title import fill_norm_title
from exporters.export_to_neo4j import export_to_neo4j
from exporters.export_to_csv import export_to_csv
# from analyze.bme3analyze import bme3analyze


def cleanup():
    loop = asyncio.get_event_loop()
    pool_futures = [[pool.close(), pool.wait_closed()][-1]
                    for pool in RedisCache.pools.values()]
    if pool_futures:
        loop.run_until_complete(asyncio.wait(pool_futures))

def startup():
    # mongo
    mongoengine.connect(config.mongo_db)
    # register cleanup
    atexit.register(cleanup)
    # ontology data

class Manage:

    def bme3load(self):
        bme3load()

    def bme3_to_ont(self):
        from owlready import onto_path
        from ont.bme3import import bme3import

        if not os.path.exists(config.ont_path):
            os.makedirs(config.ont_path)

        onto_path.append(config.ont_path)

        bme3import()

    def bme3_analyze(self):
        bme3analyze()

    def tomita(self):
        from tomita.wrap import TomitaWrap
        import re
        import html
        TAG_RE = re.compile(r'<[^>]+>')
        def remove_tags(text):
            return TAG_RE.sub('', text)

        articles = db.Article.objects.filter(first_sentence__contains='курорт')

        n = 2
        for article in articles[n:n+1]:
            # "Тяжёлый труд облагораживает хорошего человека."
            # text = html.unescape(remove_tags(article.first_sentence))
            text = article.first_sentence
            # text = "Тяжёлый труд облагораживает хорошего человека."
            result = TomitaWrap().run(text)
            print(result)

    def build_first_sentences(self):
        """Создание html с несколькими первыми предложениями в статьях
        """
        build_first_sentences()

    def dump_for_tomita(self):
        dump_for_tomita.__doc__
        dump_for_tomita()

    def extract_persons(self):
        extract_persons.__doc__
        extract_persons()

    def extract_links(self, debug_miss=False):
        extract_links.__doc__
        extract_links()

    def fill_norm_title(self):
        fill_norm_title.__doc__
        fill_norm_title()

    def rutez_paths(self):
        """Создание html с несколькими первыми предложениями в статьях
        """
        rutez_paths()

    def wtf(self):
        from rutez.rutez import Rutez
        from sklearn.feature_extraction.text import CountVectorizer
        tez = Rutez()
        with open('data/first_sentences.html') as f:
            full_text = f.read()
        vectorizer = CountVectorizer(ngram_range=(1,2))
        analyzer = vectorizer.build_analyzer()
        data = (analyzer(full_text))
        # print(type(data), len(data))

        sinsets = set()
        for item in data:
            word = item.upper()
            if word in tez.word2sinsets:
                for sinset in tez.word2sinsets[word]:
                    print(word, '|', sinset, '|', tez.upper_sinsets(sinset))
                    # sinsets.add(sinset)
        # print(sinsets)
        # print(len(sinsets))


    def reload_rutez(self):
        from rutez.rutez import Rutez
        tez = Rutez()
        tez.reload('/home/petr/ownCloud/projects/rutez/rutez.db')

    def wtf2(self):
        import nltk
        with open('data/first_sentences.html') as f:
            full_text = f.read()
        words = nltk.word_tokenize(full_text)
        my_bigrams = nltk.bigrams(words)
        # my_trigrams = nltk.trigrams(words)

    def export_to_neo4j(self):
        export_to_neo4j.__doc__
        export_to_neo4j()

    def export_to_csv(self):
        export_to_csv.__doc__
        export_to_csv()

if __name__ == '__main__':
    startup()
    fire.Fire(Manage)
