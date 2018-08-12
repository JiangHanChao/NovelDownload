-*- coding: UTF-8 -*-

# BiquegeSpider
### Author：Jianghanchao
Time：2017/9/28 completion

* 这是一个基于Python3的爬虫引擎，能够根据biqugeStory目录下story.txt文件中小说名字来抓取小说章节，所以只要将想看的小说写入进去就可以到NovelBook目录下看小说啦~\(≧▽≦)/~
鄙人第一个试手工程，基本的bug已经调完了，不好之处请多多包涵

# 工程目录：

* biqugeStory: 	主抓取程序-搜索并抓取章节链接
1. books: 		将抓取到的链接存储到这里，文件名是小说名
2. tools: 		存放一些工具函数，tmp.exe用于从 IPAgency.txt中将换行和空格清除
		   		生成一个可以被规格化打开的列表
3. __init__.py: 	包模块（空）
4. biquge.py: 		主程序，运行时运行这个即可开始抓取
5. ipAgency.txt: 	规格化ip地址
6. story.txt: 		小说搜索目录<-----从这里开始
7. UserAgent.py: 	封ip时进行代理
8. utils.py: 		工具集，用于调试输出等

* NovelBook: 		下载程序，根据链接进行下载章节,小说目录列表: 章节存放在这里
1. DownBook.py: 	主下载程序，运行biquge.py后运行这个即可
2. ipAgency.txt: 	规格化ip地址
3. UserAgent.py: 	封ip时进行代理
4. Log.txt: 		这个文件不能删，存放着下载失败的日志，可以从这里重新下载章节
5. __init__.py 		包模块（空）

* WordCloud
1. data 			文件夹
	------template	图片模板文件夹
	------stopwords.txt
2. font 			字体文件夹
3. __init__.py 		包模块（空）
4. create_word_cloud.py 	运行模块，生成图片词云

* DownloadNovel.py 	主程序运行入口

* Readme.md 		本文件

* requirement 		依赖文件包

* 思路：读取story小说名然后由搜索链接到小说，然后抓取小说主页面，下载页面的所有章节
	  链接并储存到books目录下；第二步，读取链接表并逐一从网站下载文字，并储存到
	  NovelBook目录下。

特别的：该爬虫只针对biquge网站的抓取，其他小说网站的需要重写抓取规则
另外  ：程序最好运行一次，多次会有冲突？（潜在bug）

该爬虫维护看心情吧，也许会写个用户UI界面，也许就弃坑了233（逃

end :)

# NovelDownload
download novel from biquge
move to BOOK root directory then run the cmd

## install
pip2 install -r requirement

## run
> python3 DownloadNovel.py [-h] [-w -D directory_path]/[-w -f file_path]
### 接收参数说明
* h help 帮助说明
* w WordCloud 可视化词云
* D directory 将指定目录下的txt文件作为词云输入
* f file 将指定文件作为词云输入
