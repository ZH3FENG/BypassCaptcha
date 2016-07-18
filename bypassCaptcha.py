#!/bin/bash/env python
#-*-coding:utf8-*-

##
#Time: 
#	2016-07-18
#Function:
#	bypass captcha
##

import subprocess
import urllib
import urllib2
import cookielib
import json
import md5
import time
import sys

Host = 'www.bugbank.cn'
HttpRoot = 'http://www.bugbank.cn'

class WebTool():
    
    def __init__(self,cookie=''):
		self.cookie = cookielib.LWPCookieJar()
		self.cookie_support = urllib2.HTTPCookieProcessor(self.cookie)
		self.opener = urllib2.build_opener(self.cookie_support,urllib2.HTTPHandler)
		self.header = {
            'Host': Host,		
            'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
			'Origin': HttpRoot,
			'x-client-id': 'user-web',
            'Referer': HttpRoot,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
            'Cookie': cookie
        }

    def post(self, url, data = ''):  
		urlecodedData = urllib.urlencode(data)
		request = urllib2.Request(url, urlecodedData, self.header)
		try:
			content = urllib2.urlopen(request)
			return content
		except Exception, e:
			print ("An error occured: " + str(e))
			return None
			
   
	
    def getToken(self, path = '/api/token'):
		toUrl = HttpRoot + path
		try:
			jsonContent = self.post(toUrl).read()
			dicContent = json.loads(jsonContent)
			token = dicContent['token']
			return token
		except Exception, e:
			print ("Failed to get token from server, caused by: " + str(e))
			return None
			
    def signin(self, userName, passwd, token, path='/api/signin'):
	    data = {
			'email': userName,
			'password': password,
			'token': token
		}
	    url = HttpRoot + path
	    try:
			res = self.post(url,data)
			if(res.getcode() == 200):
				authorization =  res.headers.getheader('authorization')
				print("Logined successfully!\nReceived authorization information: \n" + authorization)
			else:
				print("Oops! Something is wrong")				
	    except Exception, e:
			print ('Oops! Something is wrong. See details: ' + str(e))

	
def getUnixTime():
		toUrl = "http://s95.cnzz.com/z_stat.php?id=1259553499&web_id=1259553499&_=" + str(time.time())[0:10]
		header = {
			'Host': 's95.cnzz.com',
			'Connection': 'keep-alive',
			'Cache-Control': 'max-age=0',
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
			'Accept': '*/*',
			'Referer': 'http://www.bugbank.cn/signin.html',
			'Accept-Encoding': 'gzip, deflate, sdch',
			'Accept-Language': 'zh-CN,zh;q=0.8',
			'Cookie': 'bdpt[2]=1'
        }
		try:
			request = urllib2.Request(toUrl,headers=header)
			resp = urllib2.urlopen(request)
			if(resp.getcode()==200):
				content = resp.read()
				return content[94:104]
			else:
				print ("An error occured during get timestam from the target."+ str(resp.getcode()))
				sys.exit(1)
		except Exception, e:
			print ("An error occured: " + str(e))
			return None
			
def processToken(token_received):
	#token_received = "134baf272e4e49ff6b5c6e5f4183fdcb"
	cmd = "go run processToken.go -token=" + token_received
	data = subprocess.Popen(cmd, stdin = subprocess.PIPE, stdout = subprocess.PIPE)
	output = data.stdout.read()
	return output

if __name__ == "__main__":
	print('Login.....')
	unixTime = getUnixTime()
	addedCookie = 'CNZZDATA1259553499=859115587-1468723984-%7C' + unixTime
	web = WebTool(addedCookie)
	token_received = web.getToken()
	token_processed = processToken(token_received)
	userName = ''#your username
	passwd = ''#your password
	import hashlib   
	password = hashlib.md5(passwd).hexdigest()
	time.sleep(1)
	web.signin(userName, password, token_processed)
