'''
Created on 29 окт. 2013 г.

@author: garet
'''

import re

pattern = "\[\[\[\[\[\[[0-9]*\]\]\]\]\]\].*?\[\[\[\[\[\[\|\|\|\|\|\|\|\|\]\]\]\]\]\]"

count = 0

for i in range(0, 9):
    file_name = '/home/garet/Загрузки/3/translate_text_{0}_.html'
    file_name = file_name.format(i)
    with open(file_name, 'r') as f:
        text = f.read()
        items = re.findall(pattern, text, re.DOTALL|re.MULTILINE)
        count += len(items)
print(count)
