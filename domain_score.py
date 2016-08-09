import json
import urllib
url = 'https://www.virustotal.com/vtapi/v2/domain/report'
parameters = {'domain': '027.ru', 'apikey': 'bf4ef656d46c61f10d6184e46c702f4fd112fbd407e58c405024acd396e7e96d'}
response = urllib.urlopen('%s?%s' % (url, urllib.urlencode(parameters))).read()
response_dict = json.loads(response)
print response_dict