'''
Created on 27 окт. 2013 г.

@author: garet
'''


"""
# Add firsted items
urls = ['http://www.aliexpress.com/category/200002320/networking/1.html?needQuery=n',
        'http://www.aliexpress.com/category/100005062/tablet-pcs.html?needQuery=n&isrefine=y',
        'http://www.aliexpress.com/category/200002361/tablet-accessories.html?needQuery=n',
        'http://www.aliexpress.com/category/200002321/storage-devices.html?needQuery=n',
        'http://www.aliexpress.com/category/70803003/mini-pcs.html?needQuery=n',
        'http://www.aliexpress.com/category/200002394/accessories-parts.html',
        'http://www.aliexpress.com/category/200002397/home-audio-video.html?tracelog=allcategoriesabtestB',
        'http://www.aliexpress.com/category/200002398/portable-audio-video.html?tracelog=allcategoriesabtestB',
        'http://www.aliexpress.com/category/200002395/camera-photo.html?tracelog=allcategoriesabtestB',
        'http://www.aliexpress.com/category/200002396/video-games.html',
        'http://www.aliexpress.com/category/702/laptops.html?needQuery=n',
        'http://www.aliexpress.com/category/200002319/computer-components.html?needQuery=n',
        'http://www.aliexpress.com/category/200002395/camera-photo.html?tracelog=allcategoriesabtestB',]

def AddFirstUrls(urls):
    for url in urls:
        try:
            req = requests.get(url)
            if req.status_code == 200:
                result = model.Insert(url, \
                                      '',\
                                      TYPE_CATEGORY_0,\
                                      STATUS_NOTHING,\
                                      req.headers, \
                                      req.text)
                if result:
                    print('Complite: {0}'.format(url))
            else:
                print('Status Code: {0}, Url: {1}'.format(req.status_code, url))
        except Exception as e :
            print ('Exceptions: ', e.args)
            
#def CategoryParse(data):


url = 'http://www.aliexpress.com/category/200002395/camera-photo.html?tracelog=allcategoriesabtestB'
req = requests.get(url)
if req.status_code == 200:
    obj = AliParser.CategoryParse(url, req.text, 0)
    print(obj)
"""