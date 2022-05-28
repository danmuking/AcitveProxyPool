# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ProxyItem(scrapy.Item):
    ip = scrapy.Field()
    port = scrapy.Field()
    country = scrapy.Field()
    types = scrapy.Field()


class Builder():
    def create(self, **kwargs):
        return ProxyItem


class XiaoHuanBuilder(Builder):
    def create(self, *args) -> ProxyItem:
        item = args[0]
        item = item["item"]

        ip = item[0].xpath('.//a/text()').get()
        port = item[1].xpath('./text()').get()
        country = item[2].xpath('.//a/text()').get().split(' ')[0]
        types = item[6].xpath('.//a/text()').get()

        # 将types转为int新便于存储
        if types=='普匿':
            types = 1
        elif types == '高匿':
            types = 2

        return ProxyItem(
            ip=ip,
            port=port,
            country=country,
            types=types
        )


class Director():
    def __init__(self, builder: Builder):
        self.builder = builder

    def gen_item(self, **kwargs) -> ProxyItem:
        return self.builder.create(kwargs)
