#-- coding: utf-8 --
import pymssql
from app import conf

HOST = conf.db_host
PORT = 1433 #22
USERNAME = conf.db_user
PASSWORD = conf.db_password
DB = conf.db_database

class Mssql(object):
    def __init__(self):
        try:
            self.conn = pymssql.connect(
                server=HOST,
                user=USERNAME,
                password=PASSWORD,
                database=DB,
                port=PORT,
                charset='cp936'
            )
            self.cursor = self.conn.cursor()  # 游标对象
            print("连接数据库成功")

        except Exception as e:

            print("连接失败")
            print(e)

    def getItems(self, sql = None):
        print(sql)
        # sql = u'select top 5 * from notice order by notice_time desc'
        self.cursor.execute(sql.encode('cp936'))
        items = self.cursor.fetchall()
        # print(items)
        return items