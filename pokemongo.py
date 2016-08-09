import requests
from bs4 import BeautifulSoup
url='https://www.ispokemongoavailableyet.com'
payload={}
r=requests.get(url)
bs=BeautifulSoup(r.content,'html.parser')
bs.fin