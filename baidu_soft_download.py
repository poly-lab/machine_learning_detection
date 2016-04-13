# -*- coding: utf-8 -*-
from multiprocessing.pool import Pool
import os
import urllib
import sys

__author__ = 'liebesu'
import json
import requests
from bs4 import BeautifulSoup
import MySQLdb

def baidu_main(i):
    website='baidu'
    url='http://rj.baidu.com/soft/lists/'+str(i)
    sorts=['聊天通讯','输入法','浏览器','下载工具','影视播放','音乐播放','图像编辑','杀毒防护','压缩刻录','系统工具','驱动程序','办公学习','程序开发','股票网银','影音编辑','游戏','手机管理','桌面壁纸','网络应用']
    r=requests.get(url)
    soup=BeautifulSoup(r.text,"html.parser")
    soup_hrefall=soup.find_all('script')
    for href in soup_hrefall:
        if "var configs = " in href.get_text():
            wjson={}
            wjson=json.loads(href.get_text().lstrip().replace('var configs =  ','').replace(";",""))
            softlist=wjson['data']['softList']['list']
            for m in range(len(softlist)):
                url=softlist[m]['url']
                update_time=softlist[m]['update_time']
                point=softlist[m]['point']
                version=softlist[m]['nick_version']
                name=softlist[m]['soft_name']
                #try:
                try:
                    db= MySQLdb.connect(db="malware_info", user="root", passwd="polydata", host="localhost", port=3306,charset='utf8')
                    cursor = db.cursor()
                    reload(sys)
                    sys.setdefaultencoding('utf8')
                    insert_sql='insert into white_soft_info(Soft_Name,Soft_From,Soft_Sort,Soft_Upate_time,Soft_Point,Soft_Url) VALUES ("%s","%s","%s","%s","%s","%s") '%(name,website,sorts[i-1],update_time,point,url)
                    cursor.execute(insert_sql)
                    db.commit()
                    cursor.close()
                    db.close()
                except Exception as e:
                    cursor.close()
                    db.close()
                    print e
                    exit()
                if os.path.exists(os.path.join(os.getcwd(),website,sorts[i-1]))==False:
                    os.makedirs(os.path.join(os.getcwd(),website,sorts[i-1]))
                urllib.urlretrieve(url,os.path.join(os.getcwd(),website,sorts[i-1],os.path.basename(url.encode('utf-8'))))


if __name__=="__main__":
    a=range(1,20)
    '''for b in a:
        print b
        baidu_main(b)'''
    pool=Pool(processes=19)
    pool.map(baidu_main,a)
    pool.close()
    pool.join()
