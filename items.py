'''
Created on 25 окт. 2013 г.

@author: garet
'''

import lxml.html

class Items:
    def GetInfo(self, html_data):
        page = lxml.html.fromstring(html_data)
        return