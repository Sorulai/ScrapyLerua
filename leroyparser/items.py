# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst


def int_price(value):
    try:
        value = int(value)
    except Exception as e:
        return value
    return value


def clear_meaning(value):
    value = value.replace('\n', '').replace(' ', '')
    return value


class LeroyparserItem(scrapy.Item):
    link = scrapy.Field(output_processor=TakeFirst())
    title = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(int_price), output_processor=TakeFirst())
    photo = scrapy.Field()
    specifications_title = scrapy.Field()
    specifications_meaning = scrapy.Field(input_processor=MapCompose(clear_meaning))
    specifications = scrapy.Field()
    _id = scrapy.Field()
