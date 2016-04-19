#coding:UTF-8
import re
from urlparse import urljoin
from bs4 import BeautifulSoup
import requests

__author__ = 'liebesu'
size=''
url='http://www.xdowns.com/support/sitemap.asp'
def get_class():
    #从地图获取板块链接
    r=requests.get(url)
    soup=BeautifulSoup(r.text,"html.parser")
    categorys=soup.find_all(class_="menubar",href=re.compile("/soft/\d+/\d+/"))
    for category in categorys:
        category_name=category.string
        category_url=urljoin(url,category.get('href'))
        r_class=requests.get(category_url)
        #获取板块内软件链接
        soup_class=BeautifulSoup(r_class.text,"html.parser")
        soup_class_cas=soup_class.find(class_='p_list_7')
        sou_list_cas=BeautifulSoup(soup_class_cas.prettify(),"html.parser")
        sou_list_cags=sou_list_cas.find_all(class_="showtopic",href=re.compile('^/soft/.*?\.html$'))
        print len(sou_list_cags)
        for soup_class_ca in sou_list_cags:
            soft_page_url=urljoin(url,soup_class_ca.get('href'))
            r_soft=requests.get(soft_page_url)
            print soft_page_url
            soup_soft=BeautifulSoup(r_soft.content,"html.parser")
            try:
                print soup_soft.title.string
            except:
                title=soup_soft.find(color="#008800")
                print title.get_text().encoding('utf-8','ignore')
            soft_det=soup_soft.find(class_='meta_list')
            #获取大小、运行环境
            soft_size=[soft_det_string for soft_det_string in soft_det.stripped_strings][3]
            soft_run=[soft_det_string for soft_det_string in soft_det.stripped_strings][-1]
            if "WinAll" or "Win9x" in soft_run:
                if "KB" in soft_size:
                    soft_down=soup_soft.find(href=re.compile('^xdowns2009'))
                    print soft_down
                    soft_down_url=urljoin(url,soft_down.get('href'))
                    print soft_down_url
                    exit()

if __name__=="__main__":
    get_class()