'''
Created on 25 окт. 2013 г.

@author: garet
'''

import lxml.html


STATUS_NOTHING = 0
STATUS_IN_WORK = 1
STATUS_WELL_DONE = 2
STATUS_AFTER_DONE = 3

TYPE_CATEGORY_0 = 0
TYPE_CATEGORY_1 = 1
TYPE_CATEGORY_2 = 2
TYPE_CATEGORY_3 = 3
TYPE_CATEGORY_4 = 4
TYPE_CATEGORY_5 = 5
TYPE_ITEM_0 = 10
TYPE_ITEM_1 = 11
TYPE_ITEM_2 = 12
TYPE_ITEM_3 = 13
TYPE_ITEM_4 = 14
TYPE_ITEM_5 = 15
TYPE_IMG_0 = 20
TYPE_IMG_1 = 21
TYPE_IMG_2 = 22


class AliParser:
    @staticmethod
    def GetInfo(html_data):
        page = lxml.html.fromstring(html_data)
        return
    
    @staticmethod
    def CategoryParse(url, html_data, category_level):
        result = []
        page_tree = lxml.html.fromstring(html_data)
        category_urls = page_tree.xpath('//a[@class=" product"]')
        for url in category_urls:
            result.append({'status': STATUS_NOTHING,
                           'type': TYPE_ITEM_0,
                           'url': url.attrib['href']})
        sub_category_urls = page_tree.xpath('//div[@id="pagination-bottom"] //a')
        for url in sub_category_urls:
            result.append({'status': STATUS_NOTHING,
                           'type': category_level + 1,
                           'url': url.attrib['href']})
        return result
