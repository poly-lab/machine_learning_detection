import requests
url="http://192.168.24.168/api/v1.1/scans"
files='G:/polydata/antlab/machine_learning_detection/lvmeng_exe_5m/UPSAssistant.exe'
f={'file':open(files,'rb')}
r=requests.post(url)
print r.status_code
print r.content
'''result_url='http://192.168.24.168/api/v1.1/scans/16/results'
r=requests.get(result_url)
print r.status_code
print r.content'''