# coding: utf-8

import requests
from lxml import etree
import settings
from common import xpath_handler, gevent_download, HEADER, MY_DB
import re


def url_product():
    for i in xrange(1, 2908):
        row = MY_DB.select(settings.MFW_SQL_URL, dict(id=i))
        yield row[0][0]


def get_detail(url):
    rsp = requests.get(url=url, headers=HEADER).text
    selector = etree.HTML(rsp)
    name = xpath_handler(selector.xpath(settings.NAME_MFW))
    if name:
        print 111, name
        address, intro, comment, open, time, contact, website = list(detail_old(selector))
        print address, intro, comment, open, time, contact, website
        params = dict(
            name=name,
            address=address,
            intro=intro,
            comment=comment,
            open=open,
            time=time,
            contact=contact,
            website=website,
            url=url
        )
        MY_DB.insert(settings.QUERY_MFW, params)
    else:
        name = xpath_handler(selector.xpath(settings.NAME_MFW_NEW))
        if name:
            print 222, name
            address, intro, comment, contact, grade = list(detail_new(selector))
            print address, intro, comment, contact, grade
            params = dict(
                name=name,
                address=address,
                intro=intro,
                comment=comment,
                contact=contact,
                grade=grade,
                url=url
            )
            MY_DB.insert(settings.QUERY_MFW_NEW, params)

        else:
            print 333


def detail_new(selector):
    address = xpath_handler(selector.xpath(settings.ADDRESS_MFW_NEW))
    intro = xpath_handler(selector.xpath(settings.INTRO_MFW_NEW))
    comment = xpath_handler(selector.xpath(settings.COMMENT_MFW_NEW))
    contact = xpath_handler(selector.xpath(settings.CONTACT_MFW_NEW))
    grade = xpath_handler(selector.xpath(settings.GRADE_MFW_NEW))
    return address, intro, comment, contact, grade


def detail_old(selector):
    address = xpath_handler(selector.xpath(settings.ADDRESS_MFW))
    intro = xpath_handler(selector.xpath(settings.INTRO_MFW))
    comment = xpath_handler(selector.xpath(settings.COMMENT_MFW))
    comment = re.search('\d+', comment)
    comment = comment.group() if comment else 0
    open = xpath_handler(selector.xpath(settings.OPEN_MFW))
    time = xpath_handler(selector.xpath(settings.TIME_MFW))
    contact = xpath_handler(selector.xpath(settings.CONTACT_MFW))
    website = xpath_handler(selector.xpath(settings.WEBSITE_MFW))
    return address, intro, comment, open, time, contact, website


if __name__ == '__main__':
    gevent_download(urls=url_product(),func=get_detail)
