# coding: utf-8

import requests
from lxml import etree
import scene_settings as settings
import common
import re


def xc_scene(url):
    rsp = requests.get(url=url, headers=common.HEADER).text
    selector = etree.HTML(rsp)
    nodes = selector.xpath(settings.NODES_XC)
    for node in nodes:
        name = node.xpath(settings.NAME_XC)[0].strip()
        address = node.xpath(settings.ADDRESS_XC)[0].strip()
        grade = node.xpath(settings.SCORE_XC)[0].strip()
        comment = re.search('\d+', node.xpath(settings.COMMENT_XC)[0].strip()).group()
        url = detail_url = settings.DOMAIN_XC + node.xpath(settings.DETAIL_XC)[0].strip()
        intro, website, contact = get_detail(detail_url)
        params = dict(
            name=name.encode('utf-8'),
            address=address.encode('utf-8'),
            grade=float(grade.encode('utf-8')),
            comment=comment.encode('utf-8'),
            url=url.encode('utf-8'),
            intro=intro.encode('utf-8'),
            website=website.encode('utf-8'),
            contact=contact.encode('utf-8'),

        )
        print name
        common.MY_DB.insert(settings.QUERY_XC, params)


def get_detail(url):
    rsp = requests.get(url=url, headers=common.HEADER).text
    selector = etree.HTML(rsp)
    introduce = selector.xpath(settings.INTRODUCE_XC)
    introduce = introduce[0].strip() if introduce else ''
    website = selector.xpath(settings.WEBSITE_XC)
    website = website[0].strip() if website else ""
    phone = filter(lambda x: re.search('\d', x), selector.xpath(settings.PHONE_XC))
    phone = phone[0].strip() if phone else ''
    return introduce, website, phone


def main():
    rsp = requests.get(url=settings.SCENE_XC_URL, headers=common.HEADER).text
    selector = etree.HTML(rsp)
    pages = selector.xpath(settings.NUM_PAGE)[0].strip()
    scene_url = settings.SCENE_XC_URL[0:-5]
    for i in xrange(1, int(pages) + 1):
        raw_url = '%s/s0-p%s.html' % (scene_url, str(i))
        print raw_url
        xc_scene(raw_url)


if __name__ == '__main__':
    main()
