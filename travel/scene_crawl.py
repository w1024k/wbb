# coding: utf-8

import requests
from lxml import etree
import settings
import re


def xc_scene():
    domain = "http://you.ctrip.com"
    nodes_path = "//div[@class='list_wide_mod2']//div[@class='list_mod2']"
    name_path = ".//dt/a/text()"
    address_path = ".//dd[@class='ellipsis']/text()"
    score_path = ".//a[@class='score']/strong/text()"
    comment_path = ".//a[@class='recomment']/text()"  # (2611条点评)
    detail_url_path = ".//dt/a/@href"
    rsp = requests.get(url=settings.SCENE_XC_URL, headers=settings.HEADER).text
    selector = etree.HTML(rsp)
    nodes = selector.xpath(nodes_path)
    for node in nodes:
        name = node.xpath(name_path)[0].strip()
        address = node.xpath(address_path)[0].strip()
        score = node.xpath(score_path)[0].strip()
        comment = re.search('\d+', node.xpath(comment_path)[0].strip()).group()
        detail_url = domain + node.xpath(detail_url_path)[0].strip()
        print name
        print address
        print score
        print comment
        print detail_url
        get_detail(detail_url)
        print "============"


def get_detail(url):
    rsp = requests.get(url=url, headers=settings.HEADER).text
    selector = etree.HTML(rsp)
    introduce = selector.xpath("//div[@class='text_style']/text()")[0].strip()
    website = selector.xpath("//a[@class='breakurl']/@href")
    website = website[0].strip() if website else ""
    phone = selector.xpath("//ul[@class='s_sight_in_list']//li[1]//span[@class='s_sight_con']/text()")
    phone = phone[0].strip() if phone else ""
    print introduce
    print website
    print phone


def main():
    page_path = "//b[@class='numpage']"
    rsp = requests.get(url=settings.SCENE_XC_URL, headers=settings.HEADER).text
    selector = etree.HTML(rsp)
    pages = selector.xpath(page_path)[0].strip


if __name__ == '__main__':
    xc_scene()
