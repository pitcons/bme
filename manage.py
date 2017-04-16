# encoding: utf-8
import os
import atexit
import asyncio

import fire
import mongoengine
from aiocache import RedisCache
from owlready import onto_path

import db
from config import config
from crawlers.bme3load import bme3load
from ont.bme3import import bme3import
from analyze.bme3analyze import bme3analyze


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
    if not os.path.exists(config.ont_path):
        os.makedirs(config.ont_path)

    onto_path.append(config.ont_path)

class Manage:

    def bme3load(self):
        bme3load()

    def bme3_to_ont(self):
        bme3import()

    def bme3_analyze(self):
        bme3analyze()

    def wtf(self):
        a = db.Article.objects.all()[50]

if __name__ == '__main__':
    startup()
    fire.Fire(Manage)
