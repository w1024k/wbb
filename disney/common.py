# coding: utf-8
import MySQLdb
from gevent import monkey

monkey.patch_all()


class DB(object):
    def __init__(self):
        self.connection = MySQLdb.connect(host='localhost', port=3306, db='wbb', user='root', passwd='mysql',
                                          charset='utf8mb4')
        self.cursor = self.connection.cursor()

    @staticmethod
    def instance():
        if not hasattr(DB, "_instance"):
            DB._instance = DB()
        return DB._instance

    def insert(self, query, param={}):
        self.cursor.execute(query, param)
        self.connection.commit()

    def select(self, query, param={}):
        self.cursor.execute(query, param)
        rows = self.cursor.fetchall()
        return rows

    def close(self):
        self.cursor.close()


MY_DB = DB.instance()


def xpath_handler(data, default_val=''):
    data = data[0].strip() if data else default_val
    return data
