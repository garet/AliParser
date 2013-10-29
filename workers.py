'''
Created on 25 окт. 2013 г.

@author: garet
'''
import re

import lxml.html
from lxml.etree import tostring

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
        result = {}
        result['breadcrumb'] = ''
        result['product_name'] = ''
        result['curr_price'] = ''
        result['curr_price_type'] = ''
        result['disc_price'] = ''
        result['disc_price_type'] = ''
        result['imgs'] = []
        result['disc_price'] = ''
        result['prod_id'] = ''
        result['count_items'] = 1
        result['count_items_type'] = 'pieces'
        page_tree = lxml.html.fromstring(html_data)
        # Breadcrumb
        breadcrumb = page_tree.xpath('//div[@class="ui-breadcrumb"]')
        if len(breadcrumb) != 0:
            tmp_str = breadcrumb[0].text_content()
            tmp_str = AliParser.ClearText(tmp_str)
            tmp_str = tmp_str.replace('Home > All Categories > ', '')
            result['breadcrumb'] = AliParser.ClearText(tmp_str)
        # Product name
        product_name = page_tree.xpath('//h1[@class="product-name"]')
        if len(product_name) != 0:
            result['product_name'] = AliParser.ClearText(product_name[0].text_content())
        # Current price
        curr_price = page_tree.xpath('//dl[@class="product-info-current"] //span[@id="sku-price"]')
        if len(curr_price) != 0:
            result['curr_price'] = AliParser.ClearText(curr_price[0].text_content())
        # Current price type
        curr_price_type = page_tree.xpath('//dl[@class="product-info-current"] //span[@itemprop="priceCurrency"]')
        if len(curr_price_type) != 0:
            result['curr_price_type'] = AliParser.ClearText(curr_price_type[0].attrib['content'])
        # Discount price
        disc_price = page_tree.xpath('//dl[@class="product-info-original"] //span[@id="sku-price"]')
        if len(disc_price) != 0:
            result['disc_price'] = AliParser.ClearText(disc_price[0].text_content())
        # Discount price type
        disc_price_type = page_tree.xpath('//dl[@class="product-info-original"] //span[@itemprop="priceCurrency"]')
        if len(disc_price_type) != 0:
            result['disc_price_type'] = AliParser.ClearText(disc_price_type[0].attrib['content'])
        # Main img
        img_main = page_tree.xpath('//div[@id="img"] //img[@data-role="thumb"]')
        if len(img_main) != 0:
            result['imgs'].append(img_main[0].attrib['src'].replace('_350x350.jpg', ''))
        # Sub images
        img_sub = page_tree.xpath('//div[@id="img"] //li[@class="image-nav-item"] //img')
        if len(img_sub) != 0:
            for img in img_sub:
                img_url = img.attrib['src'].replace('_50x50.jpg', '')
                if img_url not in result['imgs']:
                    result['imgs'].append(img_url)
        # Item specific
        path = '//div[@class="ui-box ui-box-normal product-params"] ' + \
               '//dl[@class="ui-attr-list util-clearfix"]'
        item_spec_blocks = page_tree.xpath(path)
        spec_blocks = {}
        for item_spec_block in item_spec_blocks:
            dt = item_spec_block.xpath('./dt')
            dd = item_spec_block.xpath('./dd')
            if len(dt) != 0 and len(dd) != 0:
                dt = AliParser.ClearText(dt[0].text_content())
                dd = AliParser.ClearText(dd[0].text_content())
                spec_blocks[dt] = dd
        result['specification_blocks'] = spec_blocks
        # Packaging details
        path = '//div[@class="ui-box ui-box-normal pnl-packaging"] ' + \
               '//dl[@class="ui-attr-list util-clearfix"]'
        item_spec_blocks = page_tree.xpath(path)
        spec_blocks = {}
        for item_spec_block in item_spec_blocks:
            dt = item_spec_block.xpath('./dt')
            dd = item_spec_block.xpath('./dd')
            if len(dt) != 0 and len(dd) != 0:
                dt = AliParser.ClearText(dt[0].text_content())
                dd = AliParser.ClearText(dd[0].text_content())
                spec_blocks[dt] = dd
        result['packaging_details'] = spec_blocks
        # Product ID
        path = '//div[@class="prod-id"] //span'
        prod_id = page_tree.xpath(path)
        if len(prod_id) != 0:
            tmp = AliParser.ClearText(prod_id[0].text_content())
            if tmp != None:
                tmp = tmp.replace('Product ID: ', '')
            result['prod_id'] = tmp
        # Descriptions
        product_desc = page_tree.xpath('//div[@id="custom-description"] //div[@class="ui-box-body"]')
        if len(product_desc) != 0:
            tmp = lxml.html.tostring(product_desc[0])
            result['product_description_html_en'] = tmp.decode('utf-8')
        # Count items
        count_items = page_tree.xpath('//div[@id="product-info-price-pnl"] //span[@class="unit-disc sub-info"]')
        if len(count_items) != 0:
            tmp = count_items[0].text_content()
            #print(tmp)
            math = re.findall('\(([0-9]*)[\s]*([a-zA-Z]*)[\s]*/[\s]*lot', tmp)
            if len(math) > 0 and len(math[0]) == 2:
                result['count_items'] = math[0][0]
                result['count_items_type'] = math[0][1]
        return result
    
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

    @staticmethod
    def ClearText(data):
        if data != None:
            tmp_str = data.replace('\r', ' ').replace('\n', ' ')
            while tmp_str.find('  ') != -1:
                tmp_str = tmp_str.replace('  ', ' ')
            return tmp_str.strip()
        return None