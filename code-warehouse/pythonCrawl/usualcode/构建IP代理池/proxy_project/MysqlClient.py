MYSQL_HOST = 'localhost'
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PASSWORD = '999999'
MYSQL_DB = 'proxy'
MYSQL_CHARSET = 'utf8mb4'

import pymysql
import uuid

class MysqlClient(object):
    def __init__(self,host=MYSQL_HOST,port=MYSQL_PORT,user=MYSQL_USER,password=MYSQL_PASSWORD,database=MYSQL_DB,charset = MYSQL_CHARSET ):
        '''
        初始化 mysql 连接
        :param host: mysql 地址
        :param port: mysql 端口
        :param user: mysql 用户
        :param password: mysql 密码
        :param database: mysql scheme
        :param charset: 使用的字符集
        '''
        self.conn = pymysql.connect(
            host = host,
            port = port,
            user = user,
            password = password,
            database = database,
            charset = charset
        )
    def add_proxy(self,proxy):
        '''
        新增代理
        :param proxy: 代理字典
        :return:
        '''
        sql = 'insert into proxytable1 VALUES (%(id)s,%(scheme)s,%(ip)s,%(port)s,%(Anonymous_degrees)s,%(status)s,%(response_time)s,now(),null)'
        data = {
            "id":str(uuid.uuid1()),
            "scheme":proxy['scheme'],
            "ip":proxy['ip'],
            "port":proxy['port'],
            "Anonymous_degrees":proxy['Anonymous_degrees'],
            "status":proxy['status'],
            "response_time":proxy['response_time']
        }
        self.conn.cursor().execute(sql,data)
        self.conn.commit()

    def find_all(self):
        '''
        获取所有可用代理
        :return: 
        '''
        sql = 'select * from proxytable1 WHERE status = "1" order by update_date ASC'
        cursor = self.conn.cursor()
        cursor.execute(sql)
        res = cursor.fetchall()
        cursor.close()
        self.conn.commit()
        return res

    def update_proxy(self,proxy):
        '''
        更新代理信息
        :param proxy: 需要更新的代理
        :return:
        '''
        sql = 'update proxytable1 SET scheme = %(scheme)s, ip = %(ip)s, port = %(port)s, Anonymous_degrees = %(Anonymous_degrees)s,status = %(status)s, response_time = %(response_time)s, update_date = now() WHERE id = %(id)s'
        data = {
            "id":proxy['id'],
            "scheme":proxy['scheme'],
            "ip":proxy['ip'],
            "port":proxy['port'],
            "Anonymous_degrees":proxy['Anonymous_degrees'],
            "status":proxy['status'],
            "response_time":proxy['response_time']
        }
        self.conn.cursor().execute(sql,data)
        self.conn.commit()