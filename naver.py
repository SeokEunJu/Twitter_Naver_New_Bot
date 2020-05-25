import urllib.request
import requests
import os
import sys
import json

client_id=os.environ['NAVER_CLIENT_ID']
client_secret=os.environ['NAVER_CLIENT_SECRET']
 
result_title=[]
result_url=[]
result_short_url=[]

#make NAVER_API formatted url
#*args는 모든 input에 대해 같은 동작을 할 때 적합한 거 같아요
#이 함수의 인자 개수는 2개, 4개로 들어옵니다. 총 2가지 경우에요
#처음 두 인자는 지금 무슨 API를 호출한 건지 말해주고
#나머지 두 인자는 url에 넣을 keyword라서
#최소 2개의 인자를 받고 그 후에 들어오는 것은 *args로 처리해주었습니다!
def makeurl(API_type, API_name,*args):
    #news search
    if(API_type=="search"):
        if(API_name=="news"):
            search_keyword=urllib.parse.quote(args[0])
            display_num="&display="+str(args[1])
            #request json type result
            url="https://openapi.naver.com/v1/"+API_type+"/"+API_name+"?query="+search_keyword+display_num+"&sort=sim"
            return url
    #util shorturl
    if(API_type=="util"):
    	if(API_name=="shorturl"):
    	    url="https://openapi.naver.com/v1/"+API_type+"/"+API_name
    	    return url
    #wrong input format
    return 0

#attatch id and secret key to reauest header
def get_request(url):
    request=urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    return request

#get three titles and news-links
def news_links(request):
    response=urllib.request.urlopen(request)
    rescode=response.getcode()
    if(rescode==200):
        response_body=response.read()
        result_json=response_body.decode('utf-8')
        dict=json.loads(result_json)
        #originallink
        for h in dict['items']:
            result_title.append(h['title'])
            result_url.append(h['originallink'])
    #return result code. 200 is success! else failed.
    return rescode

#long url->short url
def make_short_url(result_url):
    for source in result_url:
        source_url = urllib.parse.quote(source)
        data="url="+source_url
        url = makeurl("util","shorturl")
        request=get_request(url)
        response = urllib.request.urlopen(request, data=data.encode("utf-8"))
        rescode = response.getcode()
        if(rescode==200):
            response_body=response.read()
            result_json=response_body.decode('utf-8')
            dict=json.loads(result_json)
            result_short_url.append(dict['result']['url'])
        else:
            print("Error Code:" + rescode)

def search(keyword):
    url=makeurl("search","news",keyword, 3)
    if(url==0):
        print("wrong input format")
        return
    request=get_request(url)
    rescode=news_links(request)
    if(rescode!=200):
        print("failed to get news links")
        return
    make_short_url(result_url)
    print(result_title)
    return result_short_url
    #지금의 코드는 그냥 한번 키워드 검색하고 끝나지만 나중엔 계속계속 호출을 할 거니까
    #전역변수로 설정된 list들을 초기화 시켜주었어요
    result_title.clear()
    result_url.clear()
    result_short_url.clear()
    
