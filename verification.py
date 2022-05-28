from db_util import proxy_db, redis_conn


class VerficationEngine:
    '''
    校验代理是否有效
    '''
    def __init__(self):
        """
        从数据库中抽取100条记录加入redis
        """
        # TODO: 在启动是确认redis中是否已有数据
        proxy_list = proxy_db.query(
            'proxy',
            "where is_rom=0 limit 0,100",
            'proxy', 'port'
        )
        # TODO: 修改对应数据库记录
        for each in proxy_list:
            proxy = each[0] + ':' + str(each[1])
            pair = {
                proxy : 100,
            }
            redis_conn.zadd('proxy', pair)
            proxy_db.update(
                table_name='proxy',
                condition='where proxy="{}" and port={}'.format(each[0],each[1]),
                is_rom = 1
            )


if __name__ == '__main__':
    test = VerficationEngine()
