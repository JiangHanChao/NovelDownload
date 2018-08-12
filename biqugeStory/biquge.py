# -*- coding: utf-8 -*-
#!/usr/bin/python3

from urllib.request import urlopen
from bs4 import BeautifulSoup
from .UserAgent import getlinks
from .utils import Che2ULC
import sys
import os

searchFlag = "第一章"
StoryName = "story.txt"
SearchUrl = "http://www.biquge5200.com/modules/article/search.php?searchkey="
BASE_DIR = os.path.abspath(os.path.dirname(sys.argv[0]))

def getbooklinks(book_html):
	if (book_html==None):
		return None
	bsbj = BeautifulSoup(book_html.text,"html.parser")
	return bsbj.find(id="main").findAll("td",{"class":"odd"})

def getBook(pageURL):
	html = urlopen(pageURL)
	bsbj = BeautifulSoup(html,"html.parser")
	return bsbj

def biquge_main():
	fil = open(StoryName,'r+')	#read and wirte
	bookNames = fil.readlines()
	books = []
	FirstPageFlag = False
	for line in bookNames:
		bookNamelens = len(line)
		urlline = Che2ULC(line)
		length = len(urlline)
		url = SearchUrl+urlline[0:length-3]	# remove %0A
		booklinks = getbooklinks(getlinks(url))
		if booklinks == None:
			print ("Warnning !"+urlline+" not search and found from website.")
			continue
		for link in booklinks:
			if(link.find("a")):
				href = link.contents[0].attrs['href']
				title = link.contents[0].contents[0]
				if (len(title)==(bookNamelens-1)):
					books.append(href)
					# print ("push page :"+title)
	for link in books:
		book = getBook(link).find("div",{"id":"list"}).findAll("a")
		bname = getBook(link).find(id="info").find("h1").contents[0]
		path = os.path.join(BASE_DIR,"books",bname+".txt")
		bookfp = open(path,'w',encoding='utf-8')
		for page in book:
			finaLink = page.attrs['href']
			pageName = page.contents[0]
			pos = pageName.find(searchFlag)
			if pos != -1:
				FirstPageFlag = True
			try:
				if FirstPageFlag:
					nameWithlink = pageName+'\n'+finaLink+'\n'
					bookfp.writelines(nameWithlink)
			except UnicodeEncodeError as e:
				print (e)
			else:
				continue
		bookfp.close()
		print ("Downloaded successful "+bname+" from "+link)
		FirstPageFlag = False
	fil.close()


if __name__ == '__main__':
	biquge_main()
	print ("Done biquge.py Successful !")