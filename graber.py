'''
Created on 25 окт. 2013 г.

@author: garet
'''

import csv
import datetime
import yaml
import json
import re

import urllib.request

import requests
import psycopg2

from SqlBuilder import *
from SqlMaker import *
from workers import *

import lxml.html
from lxml.html import clean

class Model:
    def __init__(self, db, type_db, pref='tbl_', debug=False):
        self.__maker = SqlMaker(conn, 'pg', pref, debug)

    def Insert(self, url, url_from, type_url, status, headers, body):
        self.__maker.Insert('{pref}allpage',
                            {'url': url},
                            {'url_from': url_from},
                            {'type': type_url},
                            {'status': status},
                            {'headers': yaml.dump(headers)},
                            {'body': body},
                            {'date_add': datetime.datetime.now()})
        return self.__maker.Execute()

    def SelectByStatus(self, type_work, status, set_type_url, set_status):
        self.__maker.Select()
        self.__maker.From('{pref}allpage')
        self.__maker.Where('type=%s', type_work)
        self.__maker.Where('status=%s', status)
        result = self.__maker.Execute()
        if not result:
            return False
        value = self.__maker.FetchOne()
        #print(value)
        if value == None:
            return False
        self.__maker.Update('{pref}allpage', 
                            {'status': set_status},
                            {'type': set_type_url})
        self.__maker.Where('id=%s', value[0])
        self.__maker.Execute()
        return value
    
    def SelectById(self, id):
        self.__maker.Select()
        self.__maker.From('{pref}allpage')
        self.__maker.Where('id=%s', id)
        result = self.__maker.Execute()
        if not result:
            return False
        value = self.__maker.FetchOne()
        return value
    
    def SelectImages(self, url):
        self.__maker.Select('data_yaml')
        self.__maker.From('{pref}allpage')
        self.__maker.Where("url_from LIKE '%%" + url + "%%'")
        result = self.__maker.Execute()
        if not result:
            return False
        value = self.__maker.FetchAll()
        return value
    
    def UpdateItemById(self, id, data):
        self.__maker.Update('{pref}allpage', 
                            {'data_yaml': data})
        self.__maker.Where('id=%s', id)
        return self.__maker.Execute()
    
    
    def UpdateStatus(self, type_work, status, set_type_url, set_status):
        self.__maker.Update('{pref}allpage', 
                            {'status': set_status},
                            {'type': set_type_url})
        self.__maker.Where('type=%s', type_work)
        self.__maker.Execute()
        
    def UpdateStatusById(self, id, set_type_url, set_status):
        self.__maker.Update('{pref}allpage', 
                            {'status': set_status},
                            {'type': set_type_url})
        self.__maker.Where('id=%s', id)
        self.__maker.Execute()
    
    def ReturnResult(self, id, set_type_url, set_status, data):
        self.__maker.Update('{pref}allpage', 
                            {'status': set_status},
                            {'type': set_type_url},
                            {'date_work': datetime.datetime.now()},
                            {'data_yaml': data})
        self.__maker.Where('id=%s', id)
        self.__maker.Execute()
    
    def Error(self, message):
        with open('error.txt', 'wt+') as f:
            f.write('{0}::{1}'.format(datetime.datetime.now(), message))


conn = psycopg2.connect(database="Aliexpress", user="garet", password="joker12")
model = Model(conn, 'pg')

model.UpdateStatus(TYPE_ITEM_0, 0, TYPE_ITEM_0, STATUS_NOTHING)

# Grabing items from link list
"""
filename = 'input.txt'
with open('input.txt', 'r') as f:
    for line in f:
        req = requests.get(line)
        if req.status_code == 200:
            result = model.Insert(line, '', TYPE_ITEM_0, STATUS_NOTHING, \
                                  req.headers, req.text)
            if result:
                print('Complite: {0}'.format(line))
            else:
                model.Error('Error SQL: {0}'.format(line))
        else:
            model.Error('Error HTTP: {0}'.format(line))
"""
"""
# Parsing info from html items
all_count = 0
i = 0
num_file = 0
item = model.SelectByStatus(TYPE_ITEM_0, 0, TYPE_ITEM_0, STATUS_IN_WORK)
while item != False:
    info = AliParser.GetInfo(item['body'])
    #print(info['product_description_html_en'])
    info['url'] = item['url']
    #for img in info['imgs']:
    #    model.Insert(img, item['url'], TYPE_IMG_0, STATUS_NOTHING, '', '')
    #    print('Complite img: {0}'.format(img))
    model.ReturnResult(item['id'],
                       TYPE_ITEM_0,
                       STATUS_WELL_DONE,
                       json.dumps(info))
    print('Complite url: {0}'.format(item['url']))
    
    with open('translate_name.txt', 'a') as f:
        f.write('[[[[[[{0}]]]]]]\r\n{1}\r\n'\
                .format(item['id'], info['product_name']))
    data_write = info['product_description_html_en']
    data_write = re.sub('(</[^>]*?>)([\s]*?)(<[^<]*?>)', '\g<1>\r\n\g<3>', data_write)
    #print(data_write)
    with open('translate_text_' + str(num_file) + '.html', 'a') as f:
        f.write('\r\n\r\n[[[[[[{0}]]]]]]\r\n\r\n{1}\r\n\r\n[[[[[[||||||||]]]]]]\r\n'\
                .format(item['id'], data_write))

    with open('category_name.txt', 'a') as f:
        f.write('[[[[[[{0}]]]]]]\r\n{1}\r\n'\
                .format(item['id'], info['breadcrumb']))
    if i == 100:
        num_file += 1
        i = -1
    i += 1
    item = model.SelectByStatus(TYPE_ITEM_0, 0, TYPE_ITEM_0, STATUS_IN_WORK)
    all_count += 1
    print(all_count)
"""
"""
url = 'http://www.aliexpress.com/item/250g-Keemun-black-tea-8-8oz-Qimen-Black-Tea-Top-Qulaity-CHQ01-Free-Shipping/540281009.html'
data = requests.get(url)
parsed = AliParser.GetInfo(data.text)
print(parsed['count_items'])
"""
# Load images
"""
def GetNum(current, max):
    result = ''
    str_curr = str(current)
    for i in range(len(str_curr), max):
        result += '0'
    for i in range(0, len(str_curr)):
        result += str_curr[i]
    return result

def LoadImage(url, name):
    urllib.request.urlretrieve(url, name)

i = 0
item = model.SelectByStatus(TYPE_IMG_0, STATUS_NOTHING, TYPE_IMG_0, STATUS_IN_WORK)
while item != False:
    name_img = '/images/{0}.jpg'.format(GetNum(i, 5))
    
    try:
        LoadImage(item['url'], '/home/garet' + name_img)
    except Exception as e:
        print('Error: {0}'.format(e.args))

    model.ReturnResult(item['id'],
                       TYPE_IMG_0,
                       STATUS_WELL_DONE,
                       name_img)
    print('Complite url: {0}'.format(item['url']))
    item = model.SelectByStatus(TYPE_IMG_0, STATUS_NOTHING, TYPE_IMG_0, STATUS_IN_WORK)
    i += 1
"""
"""
# Upload translated names
count = 0
with open('/home/garet/Загрузки/3/translate_name_.txt', 'r') as f:
    text = f.read()
    pattern = "\[\[\[\[\[\[([0-9]*)\]\]\]\]\]\]\n(.*?)\n"
    match = re.findall(pattern, text, re.DOTALL|re.MULTILINE)
    for item in match:
        id = int(item[0])
        elem = model.SelectById(id)
        if elem != False:
            data = json.loads(elem['data_yaml'])
            data['product_name_ru'] = item[1].strip()
            model.UpdateItemById(id, json.dumps(data))
            count += 1
print(count)
"""
"""
count = 0
# Upload translated category
with open('/home/garet/Загрузки/3/category_name_.txt', 'r') as f:
    text = f.read()
    pattern = "\[\[\[\[\[\[([0-9]*)\]\]\]\]\]\]\n(.*?)\n"
    match = re.findall(pattern, text, re.DOTALL|re.MULTILINE)
    print(len(match))
    for item in match:
        id = int(item[0].strip())
        name_str = item[1].replace('> ', ' > ').strip()
        elem = model.SelectById(id)
        if elem != False:
            data = json.loads(elem['data_yaml'])
            data['breadcrumb_ru'] = name_str
            model.UpdateItemById(id, json.dumps(data))
        count += 1
print(count)
"""


def _clean_attrib(node):
    for n in node:
        _clean_attrib(n)
    node.attrib.clear()

def DelParazite(data):
    tree = lxml.html.fromstring(data)
    divs = tree.xpath('//div[@style]')
    for div in divs:
        atrb = div.attrib['style']
        if atrb.find('clear: both;') != -1 or \
            atrb.find('clear:both;') != -1:
            #print(div.text)
            div.getparent().remove(div)
    return lxml.html.tostring(tree, method='html')

def ClearDescription(in_data):
    data = in_data.replace('\\t', '\t')
    data = data.replace('\\t', '\t')
    data = data.replace('\\r', '\r')
    data = data.replace('\\n', '\n')
    data = data[3:] if data[0:3] == " b'" else data
    data = data[:-1] if data[-1] == "'" else data
    data = data.strip()
    data = DelParazite(data)
    data = data.decode('utf-8')
    allow_tags = [#'table','tr','td', 'p','i','strong', 'span', 'br', 
                  'ul', 'li', 'dt','dd','dl', 'em', 'p']# 'img'
    cleaner = clean.Cleaner(allow_tags=allow_tags,
                            #remove_tags=['div',],
                            javascript = True,
                            scripts = True,
                            comments = True,
                            style = False,
                            links = True,
                            meta = True,
                            page_structure = True,
                            remove_unknown_tags=False)
    data = cleaner.clean_html(data)
    data = re.sub('(<p>[\s]*?</p>)|(<span>[\s]*?</span>)|(<span>)|(</span>)|(<strong>[\s]*?</strong>)|(<li>[\s]*?</li>)', ' ', data)
    data = re.sub('(<p></p>)|(<p>[\s]*?</p>)|(<span>[\s]*?</span>)|(<span>)|(</span>)|(<strong>[\s]*?</strong>)', ' ', data)
    data = re.sub('(<p></p>)|(<span></span>)|(<strong></strong>)|(<li></li>)', ' ', data)
    data = re.sub('>[\s]*', '>', data)
    data = re.sub('[\s]*<', '<', data)
    data = re.sub('[\s]2', ' ', data)
    data = re.sub('[\s]*<', '<', data)
    data = re.sub('[\s]*<', '<', data)
    data = re.sub('<strong', ' <strong', data)
    data = re.sub('>[\s]*?<', '><', data)
    data = re.sub('</em>', '<br/>', data)
    data = re.sub('<br>', '<br/>', data)
    data = re.sub('(<div[^>]*?>)|(</div>)', '', data)
    return data.strip()

def ClearDescription2(in_data):
    data = in_data.replace('\\t', '\t')
    data = data.replace('\\t', '\t')
    data = data.replace('\\r', '\r')
    data = data.replace('\\n', '\n')
    data = data[3:] if data[0:3] == " b'" else data
    data = data[:-1] if data[-1] == "'" else data
    data = data.strip()
    data = DelParazite(data)
    data = data.decode('utf-8')
    allow_tags = ['ul', 'li', 'dt','dd','dl', 'em', 'p']
    cleaner = clean.Cleaner(allow_tags=allow_tags,
                            javascript = True,
                            scripts = True,
                            comments = True,
                            style = True,
                            links = True,
                            meta = True,
                            page_structure = True,
                            remove_unknown_tags=False)
    data = cleaner.clean_html(data)
    data = re.sub('(<p>[\s]*?</p>)|(<span>[\s]*?</span>)|(<span>)|(</span>)|(<strong>[\s]*?</strong>)|(<li>[\s]*?</li>)', ' ', data)
    data = re.sub('(<p></p>)|(<p>[\s]*?</p>)|(<span>[\s]*?</span>)|(<span>)|(</span>)|(<strong>[\s]*?</strong>)', ' ', data)
    data = re.sub('(<p></p>)|(<span></span>)|(<strong></strong>)|(<li></li>)', ' ', data)
    data = re.sub('>[\s]*', '>', data)
    data = re.sub('[\s]*<', '<', data)
    data = re.sub('[\s]2', ' ', data)
    data = re.sub('[\s]*<', '<', data)
    data = re.sub('[\s]*<', '<', data)
    data = re.sub('<strong', ' <strong', data)
    data = re.sub('>[\s]*?<', '><', data)
    data = re.sub('</em>', '<br/>\r\n', data)
    data = re.sub('<br>', '<br/>\r\n', data)
    data = re.sub('(<div[^>]*?>)|(</div>)', '', data)
    data = re.sub('<[^/^<]*?>', '', data)
    #data = re.sub('</[^>]*>', '<br/>\r\n', data)
    data = re.sub('</[^>]*>', '\r\n', data)
    data = re.sub('<[^>]*/>', '\r\n', data)
    #print(data)
    data = RemoceSpace(data)
    #print(data)
    return data.strip()

def RemoceSpace(data):
    data_len_1 = len(data)
    data = data.replace('  ', ' ')
    data = data.replace('\n\n', '\r\n')
    data = data.replace('\r\n\r\n', '\r\n')
    data = data.replace('\r\n ', '\r\n')
    data = data.replace('\n ', '\n')
    data = data.replace('  ', ' ')
    data = data.replace('\t', ' ')
    #data = re.sub('(\n\n)|(\r\n\r\n)', '\r\n', data)
    data_len_2 = len(data)
    while data_len_1 != data_len_2:
        data_len_1 = len(data)
        data = data.replace('  ', ' ')
        data = data.replace('\n\n', '\r\n')
        data = data.replace('\r\n\r\n', '\r\n')
        data = data.replace('\r\n ', '\r\n')
        data = data.replace('\n ', '\n')
        data = data.replace('\t', ' ')
        data = data.replace('  ', ' ')
        #data = re.sub('(\n\n)|(\r\n\r\n)', '\r\n', data)
        data_len_2 = len(data)
    return data
"""
all_count = 0
for i in range(0, 9):
    count = 0
    file_name = '/home/garet/Загрузки/3/translate_text_{0}_.html'
    file_name = file_name.format(i)
    with open(file_name, 'r') as f:
        text = f.read()
        pattern = '\[\[\[\[\[\[([0-9]*)\]\]\]\]\]\](.*?)\[\[\[\[\[\[\|\|\|\|\|\|\|\|\]\]\]\]\]\]'
        matches = re.findall(pattern, text, re.DOTALL|re.MULTILINE)
        for item in matches:
            id = int(item[0])
            #if id == 1562:
            #    print(item[1])
            #descr_ru = ClearDescription(item[1])
            #print('ID:::{0}', id)
            #print(descr_ru)
            
            id = int(item[0])
            elem = model.SelectById(id)
            if elem != False:
                data = json.loads(elem['data_yaml'])
                data['product_description_html_ru'] = item[1].strip()
                model.UpdateItemById(id, json.dumps(data))
                count += 1
            else:
                print('Fuck!')
            #count += 1
    print(count)
    all_count += count
# 871
print(all_count)
"""



# Generate Output.cvs
def GetImages(url_from):
    result = []
    images = model.SelectImages(url_from)
    for img in images:
        result.append(img[0])
    if len(result) < 8:
        for i in range(len(result), 8):
            result.append('')
    return result
        
#coukl = 0
def WriteToCVS(item):
    url = item['url']
    url_from = item['url_from']
    data = json.loads(item['data_yaml'])
    images = GetImages(url)
    
    price_cur = data['curr_price'].replace('.', ',').strip()
    price_disc = data['disc_price'].replace('.', ',').strip()
    
    if price_cur != '' and price_disc != '':
        price = price_disc
    elif  price_cur != '':
        price = price_cur
    elif  price_disc != '':
        price = price_disc
        
    cvs_data = [data['product_name'].strip(),
                data['product_name_ru'].strip(),
                data['breadcrumb_ru'].strip(),
                '',
                data['count_items'],
                '',
                price,
                #data['product_description_html_en'].strip(),
                #data['product_description_html_ru'].strip(),
                ClearDescription2(data['product_description_html_en']),
                ClearDescription2(data['product_description_html_ru']),
                images[0].strip(),
                images[1].strip(),
                images[2].strip(),
                images[3].strip(),
                images[4].strip(),
                images[5].strip(),
                images[6].strip(),
                images[7].strip(),
                item['url']]
    with open('output_full_clear_2.csv', 'a', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=';',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(cvs_data)


i = 0
item = model.SelectByStatus(TYPE_ITEM_0, 0, TYPE_ITEM_0, STATUS_IN_WORK)
while item != False:
    print(item['url'])
    # Write to CVS
    WriteToCVS(item)
    # Return item
    model.UpdateStatusById(item['id'], TYPE_ITEM_0, STATUS_WELL_DONE)
    # Get next item
    item = model.SelectByStatus(TYPE_ITEM_0, 0, TYPE_ITEM_0, STATUS_IN_WORK)
    i += 1
print(i)


"""
str_m = "                         (357                          bags              / lot                                                                     ,                                                                                     US $"

math = re.findall('(\(([0-9]*)[\s]*pieces[\s]*/[\s]*lot)|(\(([0-9]*)[\s]*bags[\s]*/[\s]*lot)', str_m)
print(math)
result = math[0][1] if math[0][1] != '' else math[0][3]
print(result)
"""