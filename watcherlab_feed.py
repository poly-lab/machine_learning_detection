import os
import re
import urllib

import requests
from bs4 import BeautifulSoup
import urlparse

url='http://feed.watcherlab.com/'
r=requests.get(url)
soup=BeautifulSoup(r.content,"html.parser")
tgzs=soup.find_all(href=re.compile("watcherlab-\d"))
for tgz in tgzs:
    tgzurl=urlparse.urljoin(url,tgz.get('href'))
    if os.path.exists("watcherlab"):
        pass
    else:
        os.makedirs("watcherlab")
    urllib.urlretrieve(tgzurl,os.path.join("watcherlab",os.path.basename(tgzurl)))

