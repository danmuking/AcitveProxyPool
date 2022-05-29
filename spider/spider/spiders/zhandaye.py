from datetime import datetime

import scrapy
from scrapy.utils.response import get_base_url


class ZhandayeSpider(scrapy.Spider):
    name = 'zhandaye'
    allowed_domains = ['zdaye.com']

    def start_requests(self):
        time = datetime.now()
        # 构建开始网址
        start_url = 'https://www.zdaye.com/dayProxy/{}/{}/1.html'.format(time.year,time.month)
        # 获取最新的免费代理详情页网址
        yield scrapy.Request(url=start_url, callback=self.index_parse)

    def parse(self, response):
        print(response)

    def index_parse(self, response):
        page_url = response.xpath('//h3[@class="thread_title"]/a/@href').get()
        # 进行url拼接，将相对网址转换为完整网址
        page_url = response.urljoin(page_url)
        yield scrapy.Request(url=page_url, callback=self.parse)
