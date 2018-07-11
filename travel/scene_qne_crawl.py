# coding=utf-8

import requests
from lxml import etree
import scene_settings as settings
from common import xpath_handler, gevent_download, HEADER, MY_DB
import re


def qne_scene(url=settings.SCENE_QNE_URL):
    rsp = requests.get(url=url, headers=HEADER).text
    selector = etree.HTML(rsp)
    nodes = selector.xpath(settings.NODES_QNE)
    if nodes:
        for node in nodes:
            url = node.strip()
            get_detail(url)
    else:
        print "***warning url:%s" % url


def get_detail(url):
    rsp = requests.get(url=url, headers=HEADER).text
    selector = etree.HTML(rsp)
    name = xpath_handler(selector.xpath(settings.NAME_QNE))
    address_phone = selector.xpath(settings.ADDRESS_PHONE_QNE)
    address = address_phone[0].strip() if len(address_phone) else ''
    phone = address_phone[1].strip() if len(address_phone) > 1 else ''
    coord = xpath_handler(selector.xpath(settings.COORD))
    if coord:
        coord = coord.split(',')
        lon = coord[0]
        lat = coord[1]
    else:
        lon = lat = 0


if __name__ == '__main__':
    qne_scene()
