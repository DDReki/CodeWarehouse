MYSQL_HOST = 'localhost'
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PASSWORD = '999999'
MYSQL_DB = 'proxy'
MYSQL_CHARSET = 'utf8mb4'
import pymysql
class Mysql_Test(object):
    def __init__(self,host=MYSQL_HOST,port=MYSQL_PORT,user=MYSQL_USER,password=MYSQL_PASSWORD,database=MYSQL_DB,charset=MYSQL_CHARSET):
        self.conn = pymysql.connect(
            host = host,
            port = port,
            user = user,
            password = password,
            database = database,
            charset = charset
        )
    def get_proxy(self):
        sql = 'select scheme,ip,port from proxytable1 where status="1"'
        cursor = self.conn.cursor()
        cursor.execute(sql)
        res = cursor.fetchall()
        cursor.close
        self.conn.commit()
        return res
if __name__ == '__main__':
    Mysql_Test().get_proxy()