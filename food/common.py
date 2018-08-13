# coding: utf-8
import MySQLdb
import gevent
from gevent import monkey
import redis

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

REDIS_CLIENT = redis.Redis(host='localhost', port=6379, db=0, password='redis')

HEADER = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
}


def xpath_handler(data, default_val=''):
    data = data[0].strip() if data else default_val
    return data


def gevent_download(urls, func):
    handler_list = []
    for url in urls:
        handler_list.append(gevent.spawn(func, url))
        while len(handler_list) > 50:
            gevent.joinall(handler_list)
            handler_list = []

# 美食点来源

FOOD_XC_URL = "http://you.ctrip.com/restaurantlist/shanghai2.html"
FOOD_QNE_URL = "http://travel.qunar.com/p-cs299878-shanghai-meishi"
FOOD_MFW_URL = "http://www.mafengwo.cn/cy/10099/gonglve.html"
