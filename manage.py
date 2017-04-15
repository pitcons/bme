# encoding: utf-8
import atexit
import fire
import asyncio
import mongoengine
from aiocache import RedisCache

import db
from crawlers.bme3load import bme3load

def startup():
    mongoengine.connect('bme')
    atexit.register(cleanup)

def cleanup():
    loop = asyncio.get_event_loop()
    pool_futures = [[pool.close(), pool.wait_closed()][-1]
                    for pool in RedisCache.pools.values()]
    if pool_futures:
        loop.run_until_complete(asyncio.wait(pool_futures))

class Manage:

  def bme3load(self):
      bme3load()

  def wtf(self):
      a = db.Article.objects.all()[50]
      print(a.raw)
      print(a.title)
      print(a.url)

if __name__ == '__main__':
    startup()
    fire.Fire(Manage)
