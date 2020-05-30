import urllib.request
import requests
import os
import sys
import json
import itertools

client_id = os.environ['NAVER_CLIENT_ID']
client_secret = os.environ['NAVER_CLIENT_SECRET']
 

#attatch id and secret key to reauest header
def get_request(url):
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    return request

#make NAVER_API formatted url
def makeurl(API_type, API_name,*args):
    #news search
    if(API_type == "search"):
        if(API_name == "news"):
            search_keyword = urllib.parse.quote(args[0])
            display_num = "&display=" + str(args[1])
            #request json type result
            url = f"https://openapi.naver.com/v1/{API_type}/{API_name}?query={search_keyword}{display_num}&sort=sim"
            return url
    #util shorturl
    elif(API_type == "util"):
    	if(API_name == "shorturl"):
    	    url = f"https://openapi.naver.com/v1/{API_type}/{API_name}"
    	    return url    
    #wrong input format
    else:
        raise WrongInput


#get three titles and news-links
def news_data(request):
    result_title=[]
    result_url=[]
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    #success to get news data
    if(rescode == 200):
        response_body = response.read()
        result_json = response_body.decode('utf-8')
        loaded_json_file = json.loads(result_json)
        #originallink
        for news_json_file in loaded_json_file['items']:
            result_title.append(news_json_file['title'])
            result_url.append(news_json_file['originallink'])
        return (result_title, result_url)
    #return result code. 200 is success! else failed.
    else:
        raise FailedToLoadNews(rescode)

#long url->short url
def make_short_url(result_url):
    result_short_url=[]
    for source in result_url:
        source_url = urllib.parse.quote(source)
        data = "url="+source_url
        url = makeurl("util","shorturl")
        request = get_request(url)
        response = urllib.request.urlopen(request, data=data.encode("utf-8"))
        rescode = response.getcode()
        if(rescode == 200):
            response_body = response.read()
            result_json = response_body.decode('utf-8')
            dict = json.loads(result_json)
            result_short_url.append(dict['result']['url'])
        #return result code. 200 is success! else failed.
        else:
            raise FailedToMakeShortUrl(rescode)
    return result_short_url

def search(keyword):
    try:
        url = makeurl("search","news",keyword, 3)
    except WrongInput:
        return "makeurl 도중 오류가 발생했습니다."

    request = get_request(url)

    try:
        result_title, result_url = news_data(request)
    except FailedToLoadNews as e:
        return f"뉴스를 로드하던 중 오류가 발생했습니다.(에러코드: {e})"

    try:
        result_short_url = make_short_url(result_url)
    except FailedToMakeShortUrl as e:
        return f"URL을 변환하던 도중 오류가 발생했습니다.(에러코드: {e})"
    
    sliced_title = []
    for title in result_title:
        sliced_title.append(title[0:25]+"...")

    result = ""
    for i in range(len(sliced_title)):
        result = result + f"{sliced_title[i]}\n{result_short_url[i]} \n"
    result_title.clear()
    result_url.clear()
    result_short_url.clear()
    return result

if __name__ == "__main__":
    result=search("조지아")
    
