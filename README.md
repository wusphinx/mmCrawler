mmCrawler
=========

a python crawler to download mm pictures

For some reason,this version just can download the pictures from the websit http://www.22mm.cc/
I will do more work to make it highly abstract in few days

==================
这个爬虫是有针对一个图片网站设计的，目前还不具有通用性。
因为这个网站对图片进行了分类，每个mm隶属于不同的类别，每个mm自己又有一套图片集，因此初始思路是：找出每一个类别，每一个类别下的mm，每一个mm的图集，每一个图集下的图片url，也就是等待集齐了所有mm的所有图片url，再开始多线程下载图片，oh my god,so 慢，不能充分利用网络带宽……对应的是mm_crawler_2.py
第二种思路是：在查找分类时，就可以下载图片了。查找分类，每一个分类又有许多Page,每一个Page下又有不同mm(35)个，每一个mm又有一套图集，因为就有多线程嵌套多线程再嵌套多线程这种思路，确实下载速度杠杠的(mm_crawler.py).但是也带来一个问题，嵌套多线程不好控制，这就直接导致下载了大概四分之一的图片程序挂掉了，目前还没有找到嵌套多线程的解决方案，看看有没有其它更好的方案（必须充分利用带宽，实在忍受不了慢速），努力！
