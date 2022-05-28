import pymysql


class DBConfig:
    host = 'localhost'
    port = 3306
    db = 'active_proxy_pool'
    user = 'root'
    password = '123456'


class DBUtil:
    def __init__(self):
        self.conn = pymysql.connect(
            host=DBConfig.host,
            port=DBConfig.port,
            db=DBConfig.db,
            user=DBConfig.user,
            password=DBConfig.password
        )
        self.cursor = self.conn.cursor()
        self.create()

    def create(self):
        pass

    def insert(self, table_name: str, **kwargs):
        keys = ""
        values = ""
        for each_item in kwargs.keys():
            keys = keys + each_item + ','
            if isinstance(kwargs[each_item], str):
                values = values + "'" +kwargs[each_item]+"'" + ','
            else:
                values = values + str(kwargs[each_item]) + ','
        keys = keys[:-1]
        values = values[:-1]
        sql = '''
            insert into {} ({}) values ({}) 
        '''.format(table_name, keys, values)
        self.cursor.execute(sql)
        self.conn.commit()


class ProxyDB(DBUtil):
    def __init__(self):
        super(ProxyDB, self).__init__()

    def create(self):
        sql = """
        CREATE TABLE IF NOT EXISTS `proxy`(
            `proxy_id` INT UNSIGNED AUTO_INCREMENT,
            `proxy` VARCHAR(16) NOT NULL,
            `port` INT NOT NULL,
            `types` INT,
            `country` VARCHAR(20) DEFAULT '',
            `insert_time` DATETIME DEFAULT NOW(),
            `verification_time` DATETIME,
            `verification_nums` INT DEFAULT 0,
            `available_nums` INT DEFAULT 0,
            `is_rom` INT DEFAULT 0,
            `count` INT DEFAULT 10,
           PRIMARY KEY ( `proxy_id` )
        )ENGINE=InnoDB DEFAULT CHARSET=utf8;
        """
        self.cursor.execute(sql)
        self.conn.commit()


proxy_db = ProxyDB()

if __name__ == '__main__':
    test = ProxyDB()
    test.insert(
        table_name='proxy',
        proxy='1.1.1.1',
        port = 123,
    )
