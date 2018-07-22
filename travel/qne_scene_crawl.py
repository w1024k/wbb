# coding=utf-8

import requests
from lxml import etree
import settings
from common import xpath_handler, gevent_download, HEADER, MY_DB
import re
from common import REDIS_CLIENT
from multiprocessing import Process


def qne_scene(url=settings.SCENE_QNE_URL):
    rsp = requests.get(url=url, headers=HEADER).text
    selector = etree.HTML(rsp)
    nodes = selector.xpath(settings.NODES_QNE)
    if nodes:
        for node in nodes:
            detail_url = node.strip()
            print detail_url
            MY_DB.insert('insert into qne_url(url) VALUES (%(url)s)', dict(url=detail_url))
            # get_detail(detail_url)
            REDIS_CLIENT.set(detail_url, 1)
    else:
        print "***warning url:%s" % url


def get_detail(url):
    rsp = requests.get(url=url, headers=HEADER, proxies=get_proxy()).text

    print 'get_detail_end...'

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
    website = xpath_handler(selector.xpath(settings.WEBSITE_QNE))
    intro = xpath_handler(selector.xpath(settings.INTRO_QNE))
    if not name:
        return
    print name
    print address
    print contact
    print lon
    print lat
    try:
        grade = float(grade)
    except:
        grade = 0
    print grade
    print comment
    print open_time
    print time_advise
    print website
    print intro
    params = dict(
        name=name,
        address=address,
        grade=grade,
        comment=comment,
        url=url,
        intro=intro,
        website=website,
        contact=contact,
        lon=lon,
        lat=lat,
        open=open_time,
        time=time_advise
    )
    MY_DB.insert(settings.QUERY_QNE, params)
    # MY_DB.insert('delete from qne_url where url=%(url)s', dict(url=url))
    if name:
        REDIS_CLIENT.set(url, 0)


def url_product():
    for i in xrange(1, 201):
        yield '%s-1-%s' % (settings.SCENE_QNE_URL, str(i))


def main():
    gevent_download(urls=url_product(), func=qne_scene)


def get_proxy():
    content = requests.get("http://123.207.35.36:5010/get").content
    ip, port = content.split(":")
    proxy_address = "http://%s:%s" % (ip, port)
    proxy_attr = {"http": proxy_address}
    return proxy_attr


if __name__ == '__main__':
    # 先调main生成redis记录
    # main()
    rows = MY_DB.select('select url from qne_url')
    urls = []
    for row in rows:
        if int(REDIS_CLIENT.get(row[0])) == 0:
            print 'skip ...\n\n\n\n'
            continue
        print row[0]
        urls.append(row[0])

    while True:
        t = Process(target=gevent_download, kwargs=dict(urls=urls, func=get_detail))
        t.start()
        t.join(10)
        print 'kill ..'
        t.terminate()
