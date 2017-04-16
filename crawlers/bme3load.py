# encoding: utf-8
import re
import aiohttp
from collections import defaultdict

import asyncio
import async_timeout
from lxml import etree
from aiocache import cached, RedisCache
from aiocache.serializers import PickleSerializer
from pymongo.errors import DuplicateKeyError
from mongoengine.errors import NotUniqueError

import db
from tools.parsing import body_as_etree


cache = RedisCache(endpoint="127.0.0.1", port=6379, namespace="main")

BASE_URL = 'http://xn--90aw5c.xn--c1avg'
START_URL = BASE_URL + '/index.php/Указатель%20А-Я'


class BmeLoader:
    FETCH_TIMEOUT = 50
    ON_ERROR_SLEEP = 1

    def __init__(self):
        self.fetch_sem = asyncio.Semaphore(1)

    def cast_url(self, url):
        if url.startswith('/'):
            return BASE_URL + url
        else:
            return url

    async def fetch(self, session, url):
        url = self.cast_url(url)
        try:
            data = await cache.get(url, timeout=0)
            if data:
                return data
        #except: TimeoutError as e:
        except Exception as e:
            print(e)  # TODO

        while True:
            async with self.fetch_sem:
                with async_timeout.timeout(self.FETCH_TIMEOUT):
                    print('real fetch: ' + url)
                    async with session.get(url) as response:
                        html = await response.text()
                        if response.status == 200:
                            try:
                                await cache.set(url, html, timeout=0)
                            except Exception as e:
                            # except TimeoutError as e:
                                print(e)  # TODO

                            return html
                        await asyncio.sleep(self.ON_ERROR_SLEEP)

    async def fetch_article(self, session, url, title):
        html = await self.fetch(session, url)
        try:
            article = db.Article(url=self.cast_url(url), title=title, raw=html)
            article.save()
        except NotUniqueError:
            pass

    async def fetch_tome(self, session, url):
        root = body_as_etree(await self.fetch(session, url))
        await asyncio.wait([
            self.fetch_article(session, a.get('href'), a.get('title'))
            for a in root.xpath('//div[@class="mw-content-ltr"]//a')
        ])
        next_pages = root.xpath('//a[text()="следующие 200"]')
        if next_pages:
            await self.fetch_tome(session, next_pages[0].get('href'))

    async def run(self, loop):
        async with aiohttp.ClientSession(loop=loop) as session:
            body = body_as_etree(await self.fetch(session, START_URL))
            await asyncio.wait([
                self.fetch_tome(session, a.get('href'))
                for a in body.xpath('//a')
                if a.get('title', '').startswith('Категория')
            ])


def bme3load():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(BmeLoader().run(loop))
