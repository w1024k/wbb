# coding=utf-8

import requests
from common import HEADER, MY_DB
from lxml import etree


def get_param():
    router_url = 'http://www.mafengwo.cn/ajax/router.php'
    domain = 'http://www.mafengwo.cn'
    sql = 'insert into mfw_url(url) VALUES (%(url)s)'
    for num in xrange(1, 195):
        print num
        params = {
            'sAct': 'KMdd_StructWebAjax|GetPoisByTag',
            'iMddid': 10099,
            'iTagId': 0,
            'iPage': num
        }
        html = requests.post(url=router_url, data=params, headers=HEADER).json()
        if html.get('succ') == 1:
            html = html['data']['list']
            selector = etree.HTML(html)

            links = selector.xpath('//@href')
            for link in links:
                url = domain + link.strip()
                print url
                MY_DB.insert(sql, dict(url=url))


if __name__ == '__main__':
    get_param()
