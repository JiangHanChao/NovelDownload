#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, getopt, os
WORK_PATH = os.path.split(os.path.realpath(__file__))[0]
os.chdir(os.path.join(WORK_PATH, "NovelBook"))
from NovelBook import DownBook
os.chdir(os.path.join(WORK_PATH, "biqugeStory"))
from biqugeStory import biquge
os.chdir(WORK_PATH)

cmd = "python2 create_word_cloud.py "

def download_main(cwc, isf, path):
	biquge.biquge_main()
	DownBook.down_main()
	DownBook.ReCheck()
	print ("download novel complition.")
	if cwc:
		cwcpath = os.path.join(WORK_PATH, "WordCloud")
		os.chdir(cwcpath)
		execute = None
		if isf:
			execute = os.popen(cmd+" -f "+path, 'r', -1)
		else:
			execute = os.popen(cmd+" -D "+path, 'r', -1)
		show = execute.read()
		print (show)
		print ("create word clouds successful.")

def usage(msg="0"):
	if msg=="0":
		print ("<uasge>: ")
	else:
		print ("please input correttly: ")
	print ("	python3 <%s> [-h] [-w -D directorypath] or [-w -f filepath]" % sys.argv[0])
	print ("	h: help")
	print ("	w: create a word clouds in WordCloud directory.")
	print ("	D: get the input word's directory root to WordCloud.")
	print ("	f: get the input word's file path to WordCloud.")
	if msg!="0":
		print ("the error message: %s" % msg)
	sys.exit()

if __name__ == '__main__':
	cwc = False
	isFile = False
	filepath = []
	try:
		ops, args = getopt.getopt(sys.argv[1:], 'hD:f:w')
	except getopt.GetoptError:
		usage("GetoptError")
	for op, value in ops:
		if op == "-h":
			usage()
		elif op == "-w":
			cwc = True
		elif op == "-f":
			isFile = True
			filepath.append(value)
		elif op == "-D":
			if isFile:
				print("arguments error")
				sys.exit(1)
			else:
				filepath.append(value)
	download_main(cwc, isFile, filepath)