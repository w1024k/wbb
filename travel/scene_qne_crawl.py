# coding=utf-8

import requests
from lxml import etree
import scene_settings as settings
from common import xpath_handler, gevent_download, HEADER  # , MY_DB
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
    contact = address_phone[1].strip() if len(address_phone) > 1 else ''
    coord = xpath_handler(selector.xpath(settings.COORD_QNE))
    if coord:
        coord = coord.split(',')
        lon = coord[0]
        lat = coord[1]
    else:
        lon = lat = None
    grade = xpath_handler(selector.xpath(settings.GRADE_QNE)) or None
    comment = xpath_handler(selector.xpath(settings.COMMENT_QNE), 0)
    if comment:
        comment = re.search('\d+', comment)
        comment = comment.group() if comment else 0
    open_time = xpath_handler(selector.xpath(settings.OPEN_QNE))
    time_advise = xpath_handler(selector.xpath(settings.TIME_QNE))
    time_advise = time_advise and time_advise.split(u'：')[1]
    webiste = xpath_handler(selector.xpath(settings.WEBSITE_QNE))
    intro = xpath_handler(selector.xpath(settings.INTRO_QNE))
    print name
    print address
    print contact
    print lon
    print lat
    print grade
    print comment
    print open_time
    print time_advise
    print webiste
    print intro
if __name__ == '__main__':
    qne_scene()
