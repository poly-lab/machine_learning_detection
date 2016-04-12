import re
import requests
from bs4 import BeautifulSoup
__author__ = 'liebesu'
url='http://rj.baidu.com/soft/lists/1'

r=requests.get(url)
r.encoding='utf-8'
print r.text
soup=BeautifulSoup(r.text,"html.parser")
soup_hrefall=soup.find_all(href=re.compile('\*.exe'))
for href in soup_hrefall:
    print href
    print href.get('href')

