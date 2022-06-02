from time import sleep

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from multiprocessing import Process

from server.spider.spider.spiders.xiaohuan import XiaohuanSpider
from server.verification import VerficationEngine


class SpiderProcess(Process):  # 继承Process类
    def __init__(self, name):
        super(SpiderProcess, self).__init__()
        self.name = name

    def run(self):
        print("-"*30)
        print("爬虫进程启动")
        print("*"*30)
        process = CrawlerProcess(get_project_settings())
        process.crawl(XiaohuanSpider)
        process.start()


class VerificationProcess(Process):
    def __init__(self, name):
        super(VerificationProcess, self).__init__()
        self.name = name

    def run(self):
        sleep(10)
        print("-" * 30)
        print("代理校验进程启动")
        print("*" * 30)
        process = VerficationEngine()
        process.verficate()



