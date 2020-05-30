import itertools
import json
from myerror import *
import os
import requests
import sys
import urllib.request

class naverAPIClient:
    def __init__(self):
        self.client_id = os.environ['NAVER_CLIENT_ID']
        self.client_secret = os.environ['NAVER_CLIENT_SECRET']
 
    #attatch id and secret key to reauest header
    def get_request(self, url):
        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id",self.client_id)
        request.add_header("X-Naver-Client-Secret",self.client_secret)
        return request

    #make NAVER_API formatted url
    def makeurl(self, API_type, API_name,*args):
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
            raise SyntaxError


    #get three titles and news-links
    def get_news_data(self, request):
        result_titles=[]
        result_urls=[]
        response = urllib.request.urlopen(request)
        rescode = response.getcode()
        #success to get news data
        if(rescode == 200):
            result_json = response.read().decode('utf-8')
            loaded_json_file = json.loads(result_json)
            #load json file's news titles and original links attributes
            for news_json_file in loaded_json_file['items']:
                result_titles.append(news_json_file['title'])
                result_urls.append(news_json_file['originallink'])
            return (result_titles, result_urls)
        #failted to get new data
        else:
            raise FailedToLoadNews(rescode)

    #long url->short url
    def make_short_url(self, result_urls):
        result_short_urls=[]
        for source in result_urls:
            source_url = urllib.parse.quote(source)
            data = "url="+source_url
            url = self.makeurl("util","shorturl")
            request = self.get_request(url)
            response = urllib.request.urlopen(request, data=data.encode("utf-8"))
            rescode = response.getcode()
            if(rescode == 200):
                result_json = response.read().decode('utf-8')
                dict = json.loads(result_json)
                result_short_urls.append(dict['result']['url'])
            #return result code. 200 is success! else failed.
            else:
                raise FailedToMakeShortUrl(rescode)
        return result_short_urls

    def search(self, keyword):
        try:
            url = self.makeurl("search","news",keyword, 3)
        except SyntaxError:
            return "503 Service Unavailable"

        request = self.get_request(url)

#custom exception.py 사용

        try:
            result_titles, result_urls = self.get_news_data(request)
        except FailedToLoadNews as e:
            return f"뉴스를 로드하던 중 오류가 발생했습니다.(에러코드: {e})"

        try:
            result_short_urls = self.make_short_url(result_urls)
        except FailedToMakeShortUrl as e:
            return f"URL을 변환하던 도중 오류가 발생했습니다.(에러코드: {e})"
        
        sliced_titles = []
        for title in result_titles:
            sliced_titles.append(title[0:25]+"...")

        result = ""
        for i in range(len(sliced_titles)):
            result = result + f"{sliced_titles[i]}\n{result_short_urls[i]} \n"
        return result

        
