# coding: utf-8

import requests
from lxml import etree
from .. import settings


def xc_scene():
    rsp = requests.get(url=settings.SCENE_XC_URL, headers=settings.HEADER).text
    print rsp


if __name__ == '__main__':
    xc_scene()