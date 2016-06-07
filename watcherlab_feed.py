import os
import re
import tarfile
import urllib

import requests
import sys
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
    if os.path.exists(os.path.join("watcherlab",os.path.basename(tgzurl))):
        pass
    else:
        tgz_path=os.path.join("watcherlab", os.path.basename(tgzurl))
        urllib.urlretrieve(tgzurl,tgz_path)
        if os.path.exists("watcherlab_untaz"):
            pass
        else:
            os.makedirs("watcherlab_untaz")
        os.system("tar zxvf "+tgz_path+" -C watcherlab_untaz")
os.system('find . -name "watcherlab-email*" | xargs -i cut -f 2 -d "," {}  >watcherlab_blackemail.txt')
os.system('find . -name "watcherlab-fqdn*" | xargs -i cut -f 2 -d "," {}  >watcherlab_blackdomain.txt')
os.system('find . -name "watcherlab-ipv4*" | xargs -i cut -f 2 -d "," {}  >watcherlab_blackipv4.txt')
os.system('find . -name "watcherlab-ipv6*" | xargs -i cut -f 2 -d "," {}  >watcherlab_blackipv6.txt')
os.system('find . -name "watcherlab-md5*" | xargs -i cut -f 2 -d "," {}  >watcherlab_blackmd5.txt')
os.system('find . -name "watcherlab-url*" | xargs -i cut -f 2 -d "," {}  >watcherlab_blackurl.txt')


