#coding:UTF-8
import os
import re
import urllib
from urlparse import urljoin
from bs4 import BeautifulSoup
import requests
import MySQLdb
import sys

__author__ = 'liebesu'
website='绿盟'
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
        #获取板块内页数
        soup_class=BeautifulSoup(r_class.text,"html.parser")
        soup_page=soup_class.find(class_='page_sum')
        print category_url
        page_num=int(re.findall(r'\d+',soup_page.text)[1])
        print page_num
        category_num=category_url.encode('utf-8').split("/")[-2].zfill(3)
        for i in range(2,page_num):
            singe_page_url=urljoin(category_url,"Soft_"+category_num+"_"+str(i)+".html")
            req_class=requests.get(singe_page_url)
            soup_class=BeautifulSoup(req_class.text,"html.parser")
            soup_class_cas=soup_class.find(class_='p_list_7')
            sou_list_cas=BeautifulSoup(soup_class_cas.prettify(),"html.parser")
            sou_list_cags=sou_list_cas.find_all(class_="showtopic",href=re.compile('^/soft/.*?\.html$'))
            for soup_class_ca in sou_list_cags:
                soft_page_url=urljoin(url,soup_class_ca.get('href'))
                r_soft=requests.get(soft_page_url)
                if r_soft.status_code==200:
                    soup_soft=BeautifulSoup(r_soft.content,"lxml")
                    try:
                        title=soup_soft.title.string
                    except:
                        title=soup_soft.find(color="#008800")
                        title=title.get_text().encode('utf-8')

                    soft_det=soup_soft.find(class_='meta_list')
                    #获取大小、运行环境
                    downsite=u""
                    soft_down_url=u""
                    try:
                        soft_run=[soft_det_string for soft_det_string in soft_det.stripped_strings][-1]
                        soft_size=[soft_det_string for soft_det_string in soft_det.stripped_strings][3]
                        if "Win" in str(soft_run):
                            if "KB" in soft_size or ( "MB" in soft_size and filter(str.isdigit,str(soft_size))<5):
                                soft_idnum=filter(str.isdigit,os.path.basename(soft_page_url.encode('utf-8')))
                                soft_down_r=requests.get('http://www.xdowns.com/soft/softdownnew.asp?softid='+soft_idnum)
                                soup_soft=BeautifulSoup(soft_down_r.content,"html.parser")
                                soft_down=soup_soft.find(href=re.compile('^xdowns2009\.asp.*?downid=10'))
                                try:
                                    downsite=soft_down.get_text()
                                    urldown='http://www.xdowns.com/soft/'
                                    soft_down_url=urljoin(urldown,soft_down.get('href'))
                                except:
                                    downsite=u""

                                if soft_down_url!=u"":
                                    downloader(soft_down_url,category_name.encode('utf-8'))

                    except Exception as e:
                        print e
                        print soft_page_url
                        pass
                    database(website,title,category_name,soft_page_url,soft_size,downsite,soft_down_url)
                    '''print category_name
                    print soft_page_url
                    print title
                    print soft_run
                    print soft_size
                    print downsite
                    print soft_down_url
                    print website'''
def downloader(url,category):
    if os.path.exists(os.path.join(os.getcwd(),website,category))==False:

        os.makedirs(os.path.join(os.getcwd(),website,category))
    downurl=requests.get(url).url
    filepath=os.path.join(os.getcwd(),website,category,os.path.basename(downurl.encode('utf-8')))
    print downurl
    urllib.urlretrieve(downurl,filepath)



def database(website,title,category_name,soft_page_url,soft_size,downsite,soft_down_url):



    '''print "titile:",title.encode("utf-8")
    print "category_name:",category_name.encode("utf-8")
    print "soft_page_url:",str(soft_page_url)
    print "soft_size:",str(soft_size)
    print "downsite:",downsite.encode("utf-8")
    print "soft_down_url:",soft_down_url.encode("utf-8")
    print "website:",website'''
    db= MySQLdb.connect(db="malware_info", user="root", passwd="polydata", host="localhost", port=3306,charset='utf8')

    cursor = db.cursor()
    try:
        insert_sql='insert into lvmeng_soft_info(Soft_Name,Soft_From,Soft_Sort,Soft_detail_url,Soft_Size,Soft_down_site,Soft_Url) VALUES ' \
               '("%s","%s","%s","%s","%s","%s","%s") '%(title.encode("utf-8"),website,category_name.encode("utf-8"),str(soft_page_url),str(soft_size),downsite.encode("utf-8"),soft_down_url.encode("utf-8"))

        cursor.execute(insert_sql)
        db.commit()
        cursor.close()
        db.close()

    except Exception as e:
        cursor.close()
        db.close()
        print e
        pass 


if __name__=="__main__":
    get_class()