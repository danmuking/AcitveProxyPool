import random
from time import sleep

import requests
from datetime import datetime

from db_util import proxy_db, redis_conn
from spider.spider.settings import USER_AGENT_LIST


class Request():
    def __init__(self):
        self.user_agent_list = USER_AGENT_LIST

    def request(self):
        proxy = redis_conn.zrangebyscore('proxy', 1, 10,withscores=True)
        proxy = proxy[0]
        proxy = proxy[0].decode(encoding='utf-8')
        proxies = {
            'http': 'http://' + proxy,
            'https': 'https://' + proxy,
        }
        headers = {
            "User-Agent": random.choice(self.user_agent_list)
        }
        try:
            # TODO: 用户自定义检测网址
            res = requests.get(url='http://www.baidu.com/', proxies=proxies, headers=headers, timeout=60, verify=False)
            pair = {
                proxy: 10,
            }
            redis_conn.zadd('proxy', pair)
            is_available = True
        except Exception:
            redis_conn.zincrby('proxy', -1, proxy)
            is_available = False
        finally:
            ip, port = proxy.split(':')
            proxy_db.update(
                table_name='proxy',
                condition='where proxy="{}" and port={}'.format(ip, port),
                verification_nums=',verification_nums + 1',
                available_nums=',available_nums+1' if is_available else ',available_nums',
                verification_time=str(datetime.now().strftime('%Y/%m/%d, %H:%M:%S')),
                count=10 if is_available else ',count'
            )


class VerficationEngine:
    '''
    校验代理是否有效
    '''

    def __init__(self):
        """
        从数据库中抽取100条记录加入redis
        """
        # 启动时清空redis中缓存
        redis_conn.zremrangebyscore('proxy',-100,100)
        proxy_list = proxy_db.query(
            'proxy',
            "where is_rom=0 order by count desc limit 0,100",
            'proxy', 'port'
        )
        self.request = Request()
        for each in proxy_list:
            proxy = each[0] + ':' + str(each[1])
            pair = {
                proxy: 1,
            }
            redis_conn.zadd('proxy', pair)
            proxy_db.update(
                table_name='proxy',
                condition='where proxy="{}" and port={}'.format(each[0], each[1]),
                is_rom=1
            )

    def verficate(self):
        count = 0
        while redis_conn.zcard('proxy') != 0:
            count += 1
            if (count % 10 == 0):
                count = 0
                self._clean()
            self.request.request()
            sleep(2)

    def _clean(self):
        num = 100 - redis_conn.zcount('proxy', 1, 100)
        # TODO: 这部分可以封装成函数
        # 从数据库中抽取与失效代理对应数量的代理
        proxy_list = proxy_db.query(
            'proxy',
            "where is_rom=0 order by count desc limit 0,{}".format(num),
            'proxy', 'port'
        )

        # 加入redis
        for each in proxy_list:
            proxy = each[0] + ':' + str(each[1])
            pair = {
                proxy: 1,
            }
            redis_conn.zadd('proxy', pair)
            proxy_db.update(
                table_name='proxy',
                condition='where proxy="{}" and port={}'.format(each[0], each[1]),
                is_rom=1
            )
        # 获取失效代理
        disable_proxy_list = redis_conn.zrangebyscore('proxy', -100, 0)
        # 删除失效代理
        redis_conn.zremrangebyscore('proxy', -100, 0)
        # 修改对应数据库记录
        for each in disable_proxy_list:
            each = each.decode(encoding='utf-8')
            ip, port = each.split(':')
            proxy_db.update(
                table_name='proxy',
                condition='where proxy="{}" and port={}'.format(ip, port),
                is_rom=0,
                count=',count-1'
            )


if __name__ == '__main__':
    # test = VerficationEngine()
    # test = Request()
    # test.request()
    # redis_conn.zincrby('proxy', -1.0, '95.31.5.29:54651')
    test = VerficationEngine()
    test.verficate()
