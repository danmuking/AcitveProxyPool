import scrapy

from spider.items import XiaoHuanBuilder, Director


class XiaohuanSpider(scrapy.Spider):
    name = 'xiaohuan'
    allowed_domains = ['ip.ihuan.me']
    start_urls = ['https://ip.ihuan.me/?page=b97827cc']
    # start_urls = ['https://ip.ihuan.me/?page=77nt98997']

    def __init__(self):
        self.builder = XiaoHuanBuilder()
        self.director = Director(self.builder)

    def parse(self, response):
        proxy_list = response.xpath("//div[@class='table-responsive']").xpath(".//tbody").xpath(".//tr")
        for each in proxy_list:
            items = each.xpath(".//td")
            yield self.director.gen_item(item=items)
        if (len(proxy_list)!=0 ):
            page_list = response.xpath('//ul[@class="pagination"]//li')
            next_page = page_list[-1].xpath('.//a/@href').get()
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(url=next_page_url)
