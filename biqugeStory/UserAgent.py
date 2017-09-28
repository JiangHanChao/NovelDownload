#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import re
import random
import time
from bs4 import BeautifulSoup

headers = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
            'Accept':"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            'Accept-Encoding':'gzip',
           }

UserAgent_List = [
	"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
	"Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
	"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
	"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
	"Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
	"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
	"Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
	"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
	"Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
	"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
	"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
	"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
	"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
	"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
	"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
	"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
	"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
	"Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]

URL_test='https://www.baidu.com/'#测试IP是否可用的的网站
num_IP=7#准备采集多少个IP备用
IP_test_timeout=1#测试IP时超过多少秒不响应就舍弃了

def IP_Test(IP,URL_test,set_timeout=IP_test_timeout):#测试IP地址是否可用,时间为3秒
	try:
		requests.get(URL_test, headers=headers, proxies={'http': IP[0] }, timeout=set_timeout)
		return True
	except:
		return False

def get_IPlist(test_URl='http://t3.9laik.live/pw/'):#获取可用的IP地址
	IP_list=[]
	files = open("ipAgency.txt",'r')	#only read
	# fs = open('vaildIP.txt','w')
	IPdata = files.read()
	IPlists = re.split(' ', IPdata)
	for span in IPlists:
		span_IP = re.findall(r'\d+.\d+.\d+.\d+:\d+', span)
		if IP_Test(span_IP,test_URl):#测试通过
			IP_list.append(span_IP)
			# fs.write(span)
			# print('测试通过，IP地址为'+str(span_IP))
			if len(IP_list)>num_IP-1: #搜集够N个IP地址就行了
				print('Get vaild IP address list successful !')
				return IP_list
	files.close()
	# fs.close()
	return IP_list

IP_list=get_IPlist()

def get_random_IP():#随机获取一个IP
	ind = random.randint(0, len(IP_list)-1)
	return IP_list[ind][0]

def get_header():#获取随机的header
	return { 'User-Agent': random.choice(UserAgent_List),
             'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
             # 'Host': 'pics.dmm.co.jp',
             'Cache-Control': 'no-cache',
             'Upgrade-Insecure-Requests': '1',
             # 'Referer': 'http://f3.1024xv.com/pw/htm_data/22/1611/486610.html'
             }

count_time=3#下载图片失败时，最多使用几次代理

def getlinks(booklinks,proxy_flag=False,try_time=0):
	if not proxy_flag:	#not use agency
		try:
			book_html = requests.get(booklinks, headers=get_header(), timeout=20)
			# print('downloaded [ Directly ] book link successful.')
			time.sleep(3)
			return book_html #一次就成功下载！
		except:
			return getlinks(booklinks, proxy_flag=True)#否则调用自己，使用3次IP代理
	else:	#using agency
		if try_time<count_time:
			try:
				print('try IP agency download...')
				book_html = requests.get(booklinks, headers=get_header(), proxies={'http': get_random_IP()},timeout=20)
				print('状态码为'+str(book_html.status_code))
				if book_html.status_code==200:
					print('link downloaded by IP agency successful.')
					return book_html  # 代理成功下载！
				else:
					return  getlinks(booklinks, proxy_flag=True, try_time=(try_time + 1))
			except:
				print('IP agency failed..')
				return  getlinks(booklinks, proxy_flag=True, try_time=(try_time+1))  # 否则调用自己，使用3次IP代理
		else:
			print('links download failed except try time!')
			return None