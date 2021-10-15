# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import hashlib

import scrapy
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.python import to_bytes
from pymongo import MongoClient

from leroyparser.items import LeroyparserItem


class LeroyparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.leroymerlin

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        item['specifications'] = self.create_specific(item['specifications_meaning'], item['specifications_title'])
        del item['specifications_title']
        del item['specifications_meaning']
        collection.insert_one(item)
        return item

    def create_specific(self, meaning, title):
        data = {}
        for index, item in enumerate(title):
            data[item] = meaning[index]
        return data


class LeroyMerlinPipeLine(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photo']:
            for img in item['photo']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        item['photo'] = [itm[1] for itm in results if itm[0]]
        return item

    def file_path(self, request, response=None, info=None, *, item=LeroyparserItem):
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        return f'{item["title"]}/{image_guid}.jpg'
