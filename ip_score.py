import json
import urllib
url = 'https://www.virustotal.com/vtapi/v2/ip-address/report'
parameters = {'ip': '90.156.201.27', 'apikey': 'f938cb8607a8d497a789c47c8ad9fda85d92ad2c8bc1cc37b0d0a45cf408e4e2'}
response = urllib.urlopen('%s?%s' % (url, urllib.urlencode(parameters))).read()
response_dict = json.loads(response)
print response_dict