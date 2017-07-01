# -*- encoding: utf-8 -*-
import os

import attr
import requests
from lxml import etree

from config import config


@attr.s
class Fact:
    id = attr.ib()
    name = attr.ib()
    fields = attr.ib(default=dict)


class TomitaWrap(object):

    def run(self, text):
        response = requests.post('http://127.0.0.1:8000/run', data={'text': text})
        text = response.text
        # if '</fdo_objects>' not in text:
        #     text = text.replace('<fdo_objects>', '')

        try:
            root = etree.fromstring(text.encode('utf-8'))
        except:
            # TODO
            print('----')
            print(text.encode('utf-8'))
            print('----')
            return []

        facts_l = []
        for facts_tag in root.xpath('//facts'):
            for fact_tag in facts_tag:
                fact = Fact(name=fact_tag.tag, id=fact_tag.attrib['FactID'])
                for field in fact_tag:
                    fact.fields = {field.tag: field.attrib['val']
                                   for field in fact_tag}
                facts_l.append(fact)

        return facts_l
