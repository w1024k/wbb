# coding: utf-8
import MySQLdb
import gevent
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

    def insert(self, query, param):
        self.cursor.execute(query, param)
        self.connection.commit()

    def close(self):
        self.cursor.close()


MY_DB = DB.instance()


def xpath_handler(data):
    data = data[0].strip() if data else ''
    return data


def gevent_download(urls, func):
    handler_list = []
    for url in urls:
        handler_list.append(gevent.spawn(func, url))
        while len(handler_list) > 30:
            gevent.joinall(handler_list)
            handler_list = []


# 美食点来源
FOOD_XC_URL = "http://you.ctrip.com/restaurantlist/shanghai2.html"
FOOD_QNE_URL = "http://travel.qunar.com/p-cs299878-shanghai-meishi"
FOOD_MFW_URL = "http://www.mafengwo.cn/cy/10099/gonglve.html"

# 住宿
HOTEL_XC_URL = "http://hotels.ctrip.com/hotel/Shanghai2"
HOTEL_QNE_URL = "http://travel.qunar.com/p-cs299878-shanghai-meishi"
HOTEL_MEW_URL = "http://www.mafengwo.cn/hotel/10099/?sFrom=mdd"

# 购物
SHOP_XC_URL = "http://you.ctrip.com/shoppinglist/Shanghai2.html?ordertype=0"
SHOP_QNE_URL = "http://travel.qunar.com/p-cs299878-shanghai-meishi"
SHOP_MEW_URL = "http://www.mafengwo.cn/gw/10099/gonglve.html"

# 娱乐
PLAY_QNE_URL = "http://travel.qunar.com/p-cs299878-shanghai-meishi"
PLAY_MFW_URL = "http://www.mafengwo.cn/yl/10099/gonglve.html"

HEADER = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
}

# XC_URL = 'http://you.ctrip.com/journeys/Shanghai2/t1.html'
# MFW_URL = 'http://www.mafengwo.cn/xc/10099/'
# QNE_URL = 'http://travel.qunar.com/travelbook/list/22-shanghai-299878/start_heat/1.htm'
# BD_URL = 'https://lvyou.baidu.com/plan/counselor?surls[]=shanghai&days_cnt_low=&days_cnt_high='
