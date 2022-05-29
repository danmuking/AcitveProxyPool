from time import sleep

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from multiprocessing import Process

from spider.spider.spiders.xiaohuan import XiaohuanSpider
from verification import VerficationEngine


class SpiderProcess(Process):  # 继承Process类
    def __init__(self, name):
        super(SpiderProcess, self).__init__()
        self.name = name

    def run(self):
        process = CrawlerProcess(get_project_settings())
        process.crawl(XiaohuanSpider)
        process.start()


class VerificationProcess(Process):
    def __init__(self, name):
        super(VerificationProcess, self).__init__()
        self.name = name

    def run(self):
        sleep(10)
        process = VerficationEngine()
        process.verficate()


if __name__ == '__main__':
    process_list = []
    spider_process = SpiderProcess("spider")
    spider_process.start()
    verification_process = VerificationProcess('verification')
    verification_process.run()

