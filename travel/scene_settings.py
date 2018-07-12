# coding: utf-8

# 景点来源
SCENE_XC_URL = "http://you.ctrip.com/sight/shanghai2.html"
SCENE_QNE_URL = "http://travel.qunar.com/p-cs299878-shanghai-jingdian"
SCENE_MFW_URL = "http://www.mafengwo.cn/jd/10099/gonglve.html"

# xpath_xc
NUM_PAGE = "//b[@class='numpage']/text()"

DOMAIN_XC = "http://you.ctrip.com"
NODES_XC = "//div[@class='list_wide_mod2']//div[@class='list_mod2']"
NAME_XC = ".//dt/a/text()"
ADDRESS_XC = ".//dd[@class='ellipsis']/text()"
SCORE_XC = ".//a[@class='score']/strong/text()"
COMMENT_XC = ".//a[@class='recomment']/text()"  # (2611条点评)
DETAIL_XC = ".//dt/a/@href"

# detail_xc
INTRODUCE_XC = "//div[@class='text_style']/text()"
WEBSITE_XC = "//a[@class='breakurl']/@href"
PHONE_XC = "//ul[@class='s_sight_in_list']//li//span[@class='s_sight_con']/text()"

QUERY_XC = """insert into xc_scenic(
                    name,
                    address,
                    grade,
                    comment,
                    url,
                    intro,
                    website,
                    contact)
              values(
                    %(name)s,
                    %(address)s,
                    %(grade)s,
                    %(comment)s,
                    %(url)s,
                    %(intro)s,
                    %(website)s,
                    %(contact)s)
            """

# 去哪儿

DOMAIN_QNE = "http://travel.qunar.com/"
NODES_QNE = "//ul[@class='list_item clrfix']//li//a[@class='titlink']/@href"
NAME_QNE = "//h1[@class='tit']/text()"
ADDRESS_PHONE_QNE = "//td[@class='td_l']//dd/span/text()"
COORD_QNE = "//div[@class='mapbox']/@latlng"
GRADE_QNE = "//span[@class='cur_score']/text()"
COMMENT_QNE = "//a[@class='more']/text()"
OPEN_QNE = "//dl[@class='m_desc_right_col']//span/p/text()"
TIME_QNE = "//div[@class='time']/text()"
WEBSITE_QNE = "//dd[@class='m_desc_isurl']/a/@href"
INTRO_QNE = "//div[@class='e_db_content_box']//p/text()"