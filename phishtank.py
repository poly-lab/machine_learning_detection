
from urlparse import  urljoin

import requests
from bs4 import BeautifulSoup
import MySQLdb
baseurl='http://www.phishtank.com/phish_archive.php'
detailurl='http://www.phishtank.com/phish_detail.php'
payloads={'page':0}
r=requests.get(baseurl,params=payloads)
if r.status_code==200:
    soup=BeautifulSoup(r.content,"html.parser")
    tables=soup.find_all(style="background: #ffffff;")
    for table in tables:
        strings=[string for string in table.strings]
        print strings
        print strings[0],strings[2],strings[3],strings[4],strings[5]
        r=requests.get(detailurl,params=strings[0])

def intodb():
    db=MySQLdb.connect(db="domain", user="root", passwd="polydata", host="localhost", port=3306,charset='utf8')
    cursor=db.cursor()
    try:
        sql='insert into phishtank '
    except Exception as e:
        print e

