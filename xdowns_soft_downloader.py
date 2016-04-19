import re
from urlparse import urljoin
from bs4 import BeautifulSoup
import requests

__author__ = 'liebesu'
size=''
url='http://www.xdowns.com/support/sitemap.asp'
def get_class():
    r=requests.get(url)
    soup=BeautifulSoup(r.text,"html.parser")
    categorys=soup.find_all(href=re.compile("/soft/\d"))
    print len(categorys)
    for category in categorys:
        category_name=category.string
        category_url=urljoin(url,category.get('href'))
        print category_url
        r_class=requests.get(category_url)
        soup_class=BeautifulSoup(r_class.text,"html.parser")
        soup_class_cas=soup_class.find_all(href=re.compile('^/soft/(.*?)html$'))
        for soup_class_ca in soup_class_cas:
            #print urljoin(url,soup_class_ca.get('href'))
            pass

if __name__=="__main__":
    get_class()