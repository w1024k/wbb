# coding: utf-8

import requests
from lxml import etree
import settings
from common import xpath_handler, MY_DB
from threading import Thread
import copy, gevent
import gevent
from gevent import monkey

monkey.patch_all()


def handler():
    for i in range(1, 6):
        params = copy.copy(settings.PARAMS)
        params['star'] = str(i)
        pages = get_page(params)
        print pages
        worker(params, pages)
        # 使用多线程
        # t = Thread(target=worker, args=(params, pages))
        # t.start()


def worker(params, pages):
    print 'pages:%s' % pages
    level = int(params['star'])
    spider_list = []
    for page_num in range(1, pages + 1):
        spider_list.append(gevent.spawn(spider, params, level, page_num))
        print 'pagenow:%s,level:%s' % (page_num, level)
        # 使用协成
        while len(spider_list) > 50 or page_num == pages:
            gevent.joinall(spider_list)
            spider_list = []
            if page_num == pages:
                break


def spider(params, level, page_num):
    params['pagenow'] = page_num
    rsp = requests.post(url=settings.COMMENT_URL, headers=settings.HEADER, params=params).text
    selector = etree.HTML(rsp)
    nodes = selector.xpath(settings.ROOT_PATH)
    for node in nodes:
        record = dict(
            nick=xpath_handler(node.xpath(settings.NICK_PATH)),
            date=xpath_handler(node.xpath(settings.DATE_PATH)),
            comment=xpath_handler(node.xpath(settings.COMMENT_PATH)),
            level=level,
        )
        # print level, record['nick']
        MY_DB.insert(settings.SQL_QUERY, record)


def get_page(params):
    rsp = requests.post(url=settings.COMMENT_URL, headers=settings.HEADER, params=params).text
    selector = etree.HTML(rsp)
    page = selector.xpath(settings.PAGE_PATH)
    return int(xpath_handler(page, default_val=1))


if __name__ == '__main__':
    handler()
