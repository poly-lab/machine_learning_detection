import requests

url='https://192.168.24.101/garuda/downloadTaskReport.do?taskreportid=114'
url='https://192.168.24.101'
r=requests.post(url,cert=('G:/polydata/antlab/machine_learning_detection/cert/1.cer'),verify=True)
print r.content
