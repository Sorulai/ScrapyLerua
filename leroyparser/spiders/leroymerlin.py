import scrapy
from scrapy.http import HtmlResponse
from leroyparser.items import LeroyparserItem
from scrapy.loader import ItemLoader


class LeroymerlinSpider(scrapy.Spider):
    name = 'leroymerlin'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, query):
        super().__init__()
        self.start_urls = [f'https://nizhniy-novgorod.leroymerlin.ru/search/?q={query}']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath('//a[@data-qa-pagination-item="right"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath('//a[@data-qa="product-name"]')
        for link in links:
            yield response.follow(link, callback=self.parse_products)

    def parse_products(self, response: HtmlResponse):
        loader = ItemLoader(item=LeroyparserItem(), response=response)

        loader.add_value('link', response.url)
        loader.add_xpath('title', '//h1[@slot="title"]/text()')
        loader.add_xpath('price', '//span[@slot="price"]/text()')
        loader.add_xpath('photo',
                         '//picture[@slot="pictures"]/source[@media=" only screen and (min-width: 1024px)"]/@srcset')
        loader.add_xpath('specifications_title', '//dt[@class="def-list__term"]/text()')
        loader.add_xpath('specifications_meaning', '//dd[@class="def-list__definition"]/text()')
        yield loader.load_item()
