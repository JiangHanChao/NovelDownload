<<<<<<< HEAD
# -*- coding: UTF-8 -*-

Author：Jianghanchao
Time：2017/9/28 completion

这是一个基于Python3的爬虫引擎，能够根据biqugeStory目录下story.txt文件中
小说名字来抓取小说章节，所以只要将想看的小说写入进去就可以到NovelBook
目录下看小说啦~\(≧▽≦)/~
鄙人第一个试手工程，基本的bug已经调完了，不好之处请多多原谅

工程目录：

biqugeStory: 	主抓取程序-搜索并抓取章节链接
	books: 		将抓取到的链接存储到这里，文件名是小说名
	tools: 		存放一些工具函数，tmp.exe用于从IPAgency.txt中将换行和空格清除
		   		生成一个可以被规格化打开的列表
	__init__.py: 	包模块（空）
	biquge.py: 		主程序，运行时运行这个即可开始抓取
	ipAgency.txt: 	规格化ip地址
	story.txt: 		小说搜索目录<-----从这里开始
	UserAgent.py: 	封ip时进行代理
	utils.py: 		工具集，用于调试输出等

NovelBook: 		下载程序，根据链接进行下载章节
	<list>
		小说目录列表: 章节存放在这里
	</list>
	DownBook.py: 	主下载程序，运行biquge.py后运行这个即可
	ipAgency.txt: 	规格化ip地址
	UserAgent.py: 	封ip时进行代理
	Log.txt: 		这个文件不能删，存放着下载失败的日志，可以从这里重新下载章节

思路：读取story小说名然后由搜索链接到小说，然后抓取小说主页面，下载页面的所有章节
	  链接并储存到books目录下；第二步，读取链接表并逐一从网站下载文字，并储存到
	  NovelBook目录下。

特别的：该爬虫只针对biquge网站的抓取，其他小说网站的需要重写抓取规则
另外  ：程序最好运行一次，多次会有冲突？（潜在bug）

该爬虫维护看心情吧，也许会写个用户UI界面，也许就弃坑了233（逃

README.md----end
=======
# NovelDownload
download novel from biquge
>>>>>>> d1c0a62e47b37902f267471274f1a5760b396a09
