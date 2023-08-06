import requests

url = "https://usw5.dm-us.informaticacloud.com/saas/public/core/v3/import/package"

payload={}
files=[
  {'package':open('C:\Users\ppradeep\Downloads\\response.zip','rb')}
]
headers = {
  'INFA-SESSION-ID': '2o0ojchWcdLcUL5RqbOsGA',
  'Content-Type': 'multipart/form-data'
}

response = requests.request("POST", url, headers=headers, data=payload, files=files)

print(response.text)
