# encoding = utf-8
#!/usr/bin/python3

from urllib.request import urlopen
from bs4 import BeautifulSoup
from UserAgent import getlinks
from UserAgent import CheckLog
import string
import urllib
import time
import requests
import re
import sys
import os

FILE_DIR = os.path.abspath(os.path.dirname(sys.argv[0]))
nulllist = []

# 工具集
# def PrintObj(obj):
# 	print ('\n'.join(['%s:%s' % item for item in obj.__dict__.items()]))

# def log(messge, from_=None):
# 	if from_ == None:
# 		print (str(messge))
# 	else:
# 		print (str(from_)+" : "+str(messge))

def SearchFiles(path, filemod = True):
	filelist = []
	dirlist  = []
	allLists = os.listdir(path)
	for fil in allLists:
		if os.path.isdir(path + '\\' + fil):
			if (fil[0] != '.'):
				dirlist.append(fil)
		if(os.path.isfile(path + '\\' + fil)):
			filelist.append(fil)
	if filemod:
		return filelist
	else:
		return dirlist

def DownloadChapt(chapterlink):
	# log(chapterlink,"chapterlink")
	chap = getlinks(chapterlink)
	if chap == None:
		print (chapterlink+" download failed.")
		return None
	return BeautifulSoup(chap.text,"html.parser")

def get_format_filename(input_filename): #文件夹的名字不能含有的特殊符号，windows下的限定
	for s in ['?', '*', '<', '>', '\★', '|', '"']:
		while s in input_filename:
			input_filename = input_filename.strip().replace(s, '')
	if input_filename.find('@') == -1:
		return input_filename
	# rule for miao jiang gu shi two romove '为@XXX'
	for i in ["为@","@为","位@","@位"]:
		if i in input_filename:
			pos = input_filename.find(i)
			return input_filename[0:pos-1]
	# exist '@' in string but not above
	print ("the name has error in "+input_filename+" IGNORE for split @ to end")
	return input_filename[0:input_filename.find('@')]

def get_LatestTimeFile(folderpath):
	filelist = SearchFiles(folderpath)
	latestfile = folderpath
	if filelist == nulllist:  
		return None
	new = 0.0
	for f in filelist:
		fpath = os.path.join(folderpath,f)
		t = os.path.getmtime(fpath)
		if t > new:
			new = t
			latestfile = fpath
	return latestfile

def main():
	DownDir = os.path.join(FILE_DIR,"..\\biqugeStory","books")
	if not os.path.isdir(DownDir):
		print ("Error : the novel dir is not exist !")
		exit(-1)
	# print ("get novel dir...")
	fileList = SearchFiles(DownDir)
	bookpath = []
	bookdir  = []
	for book in fileList:
		bookpath.append(os.path.join(DownDir,book))
		currpath = os.path.join(FILE_DIR, book[0:len(book)-4])
		if not os.path.exists(currpath):
			os.mkdir(currpath)
		bookdir.append(currpath)
	for i in range(len(bookpath)):
		novel = open(bookpath[i], 'r', encoding='utf-8')  #only read
		bookchapter = novel.readlines()
		novel.close()
		lens = len(bookchapter)
		Curpath = bookdir[i]
		latestf = get_LatestTimeFile(Curpath)
		updataFlag = False
		if latestf == None:
			updataFlag = True
		for x in range(0,lens,2):
			name = get_format_filename(bookchapter[x][0:len(bookchapter[x])-1])
			formatName = os.path.join(Curpath,name+'.txt')
			if latestf == formatName:
				updataFlag = True
			if not updataFlag:
				continue
			chaptebs = DownloadChapt(bookchapter[x+1][0:len(bookchapter[x+1])-1])  #remove '\n'
			chapter = chaptebs.find("div",id="content")
			if (chapter == None)or(chapter.contents == nulllist):
				errf = open(os.path.join(FILE_DIR,"Log.txt"), 'a', encoding='utf-8')  #write by appending
				errf.write("Missing Chapter Error: Lack page >>"+formatName+'\n')
				errf.close()
				continue
			# print (str(chapter.contents[0]))
			f = open(formatName,'w',encoding='utf-8')  #only write
			start = 0
			if str(chapter.contents[0]) == "<br/>":
				start = 1
			for y in range(start,len(chapter.contents),2):
				f.write(str(chapter.contents[y])+'\n')
			f.close()
		print (str(bookpath[i])+" download complete.")
		updataFlag = False


def ReCheck(): 
	CheckDir = os.path.join(FILE_DIR,"..\\biqugeStory","books")
	logpath = os.path.join(FILE_DIR,"Log.txt")
	lacklist = CheckLog(logpath)
	errf = []
	u3000list = []
	if lacklist == -1:
		print ("No find Lack Chapter in Log .GOOD")
		return
	for lac in lacklist:
		cname = os.path.split(lac)[1]
		chaptername = cname[0:len(cname)-5]+'\n'
		lackbookname = os.path.split(lac)[0].split("\\")[3]
		lackpath = os.path.join(CheckDir,lackbookname+".txt")
		lackf = open(lackpath,'r',encoding='utf-8')
		chapterlist = lackf.readlines()
		lackf.close()
		pos = chapterlist.index(chaptername)
		relink = chapterlist[pos+1][0:len(chapterlist[pos+1])-1]
		reChapterbs = DownloadChapt(relink)
		reChapter = reChapterbs.find("div",id="content")
		if (reChapter == None):
			print("Failed: "+lackbookname+" in "+chaptername[0:len(chaptername)-1])
			errf.append(lac)
			continue
		if (reChapter.contents == nulllist):
			txts = reChapterbs.text
			pos = txts.find("\u3000\u3000")
			end = txts.find("bdshare()")
			u3000list = txts[pos:end].split("\u3000\u3000")
		currp = lac[0:len(lac)-1]
		f = open(currp,'w',encoding='utf-8')  #only write
		if u3000list != []:
			for w in u3000list:
				if w == '' or w == '\n\n':
					continue
				f.write("\u3000\u3000"+w+'\n')
		else:
			s_t = 0
			if str(reChapter.contents[0]) == "<br/>":
				s_t = 1
			for y in range(s_t,len(reChapter.contents),2):
				f.write(str(reChapter.contents[y])+'\n')
		f.close()
		print("redownload successful.")

	print("relog updata ...")
	f = open("Log.txt",'w',encoding = 'utf-8')
	for err in errf:
		f.write("Missing Chapter Error: Lack page >>"+err)	 #save modify time for raw time
	f.close()
	print("ReCheckLog complete.")


if __name__ == '__main__':
	main()
	ReCheck()