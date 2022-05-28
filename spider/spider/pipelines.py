# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from db_util import proxy_db
from ..spider.items import ProxyItem


class SpiderPipeline:
    def process_item(self, item, spider):
        return item


class ProxyPipeline:
    """
    数据持久化流程
    """

    def process_item(self, item: ProxyItem, spider):
        table_name = 'proxy'
        proxy_db.insert(
            table_name=table_name,
            proxy=item.get('ip'),
            port=item.get('port'),
            country=item.get('country'),
            types=item.get('types')
        )
        return item
