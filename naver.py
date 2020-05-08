import urllib.request
import requests
import os
import sys
import json

client_id='Your_client_id'
client_secret='Your_client_secret'
result_url=[]
result_short_url=[]
params={'query':'남양','display':'3'}
search_keyword=urllib.parse.quote("남양")
display_num="&display=3"
url="https://openapi.naver.com/v1/search/news?query="+search_keyword+display_num
#json 결과
# url = "https://openapi.naver.com/v1/search/blog.xml?query=" + encText # xml 결과

request=urllib.request.Request(url)
request.add_header("X-Naver-Client-Id",client_id)
request.add_header("X-Naver-Client-Secret",client_secret)
response=urllib.request.urlopen(request)
rescode=response.getcode()
if(rescode==200):
    response_body=response.read()
#print(response_body.decode('utf-8'))
#print(type(response_body))->byte
#print(type(response_body.decode('utf-8')))->str
    result_json=response_body.decode('utf-8')
    dict=json.loads(result_json)
#originallink
    for h in dict['items']:
        result_url.append(h['originallink'])
else:
    print("Error Code:" + rescode)

for source in result_url:
    source_url = urllib.parse.quote(source)
    data="url="+source_url
    url = "https://openapi.naver.com/v1/util/shorturl"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    rescode = response.getcode()
    if(rescode==200):
        response_body=response.read()
        result_json=response_body.decode('utf-8')
        dict=json.loads(result_json)
        result_short_url.append(dict['result']['url'])
    else:
        print("Error Code:" + rescode)
print(result_short_url)
