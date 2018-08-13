# coding: utf-8

import requests
from lxml import etree
import common
from common import xpath_handler, gevent_download, HEADER, MY_DB
import re


# 基本信息
def xc_scene(url):
    rsp = requests.get(url=url, headers=HEADER).text
    selector = etree.HTML(rsp)
    nodes = selector.xpath(settings.NODES_XC)
    if nodes:
        for node in nodes:
            name = xpath_handler(node.xpath(settings.NAME_XC))
            address = xpath_handler(node.xpath(settings.ADDRESS_XC))
            grade = xpath_handler(node.xpath(settings.SCORE_XC))
            comment = re.search('\d+', xpath_handler(node.xpath(settings.COMMENT_XC)))
            comment = comment.group() if comment else 0
            url = detail_url = settings.DOMAIN_XC + xpath_handler(node.xpath(settings.DETAIL_XC))
            intro, website, contact = get_detail(detail_url)
            params = dict(
                name=name.encode('utf-8'),
                address=address.encode('utf-8'),
                grade=float(grade.encode('utf-8')) if grade else 0,
                comment=comment.encode('utf-8'),
                url=url.encode('utf-8'),
                intro=intro.encode('utf-8'),
                website=website.encode('utf-8'),
                contact=contact.encode('utf-8'),

            )
            print name
            MY_DB.insert(settings.QUERY_XC, params)
    else:
        print "***warning url:%s" % url


# 详细信息
def get_detail(url):
    rsp = requests.get(url=url, headers=HEADER).text
    selector = etree.HTML(rsp)
    introduce = xpath_handler(selector.xpath(settings.INTRODUCE_XC))
    website = xpath_handler(selector.xpath(settings.WEBSITE_XC))
    phone = xpath_handler(filter(lambda x: re.search('\d', x), selector.xpath(settings.PHONE_XC)))
    return introduce, website, phone


# 链接生成器
def url_product():
    for i in xrange(1, 10813):
        yield '%s/s0-p%s.html' % (common.FOOD_XC_URL, str(i))


def main():
    gevent_download(urls=url_product(), func=xc_scene)


if __name__ == '__main__':
    main()
