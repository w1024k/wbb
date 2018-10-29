# coding: utf-8

COMMENT_URL = "http://you.ctrip.com/destinationsite/TTDSecond/SharedView/AsynCommentView"

PAGE_PATH = '//b[@class="numpage"]/text()'
ROOT_PATH = '//div[@class="comment_single"]'
COMMENT_PATH = './/li[@itemprop="description"]/span/text()'
NICK_PATH = './/a[@itemprop="author"]/text()'
DATE_PATH = './/em[@itemprop="datePublished"]/text()'
PARAMS = {
    "poiID": "13412802",
    "districtId": "2",
    "districtEName": "ShanghaiDisneyResort",
    "pagenow": "1",
    "order": "3.0",
    "star": "0.0",
    "tourist": "0.0",
    "resourceId": "1412255",
    "resourcetype": "2",

}

HEADER = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
}

SQL_QUERY = """insert into travel_comment(
                    nick,
                    date,
                    comment,
                    level)
              values(
                    %(nick)s,
                    %(date)s,
                    %(comment)s,
                    %(level)s)
            """
