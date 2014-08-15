#-*-coding:utf-8-*-
from BeautifulSoup import BeautifulSoup
import requests
import os,sys
import re
import urllib
import threading
import Queue
from multiprocessing.pool import ThreadPool
from multiprocessing import Pool,Queue,Process
#
main_url = 'http://www.22mm.cc'
page_pre = 'index_'
save_path = '/root/Desktop/picture2/'
#
proxylist = (
            '211.167.112.14:80',
            '115.47.8.39:80',
            )

def getSoup(url,proxylist = proxylist):
    for i in proxylist:
        proxy = {'':i}
        opener = urllib.FancyURLopener(proxy)
        html = opener.open(url).read()
        soup = BeautifulSoup(html)
    return soup

#get all fenlei url
def get_fenlei_url(url):
    soup = getSoup(url)
    result = soup.find('div',{'class':'inner_menu'}).findAll('a',{'href':re.compile("/mm.*/$")})
    result = [url + i.get('href') for i in result]
    return result

#get real pic url which is end with .jpg
def get_pic_url(url):
    soup = getSoup(url)
    result = soup.findAll('script')
    mm = result[6].getString
    cc = str(mm).split('"')[-2]
    cc = cc.replace('big','pic')
    return cc

#download one pic
def download_pic(url,path = save_path):
    r = requests.get(url)
    path = path + str(url).split('/')[-1]
    urllib.urlretrieve(url,path)

#get person from page    
def get_page_all_person(page,main_url = main_url):
    soup = getSoup(page)
    pic_tag = soup.find('div',{'class':'topBox'}).findNextSiblings('div',{'class':'c_inner'})
    pic_tag = pic_tag[0].findAll('ul',{'class':'pic'})
    result = list()
    for i in pic_tag:
        tmp = i.findAll('a')
        for j in tmp:
            result.append(j.get('href'))
    g = lambda x:main_url + x
    result = map(g,result)
    return result
#
def get_person_pic_url_Set(person_url):
    soup = getSoup(person_url)
    tag = soup.find('div',{'class':'pagelist'}).findAll('a')
    result = [i.get('href') for i in tag]
    pre = '/'.join(person_url.split('/')[:-1]) + '/'
    g = lambda x:pre + x
    result = map(g,result)
    result[0] = person_url
    result.pop()
    result = map(get_pic_url,result)
    return result
    
def dowload_person(person_url):
    person_pic_url = get_person_pic_url_Set(person_url)
    map(download_pic,person_pic_url)

def download_from_page(page_url):
    page_persons = get_page_all_person(page_url)
    map(dowload_person,page_persons)

def get_fenlei_allpage(fenlei,page_pre = page_pre):
    url = fenlei
    allpage = list()
    next = 2
    while True:
        r = requests.get(url)
        if r.status_code == 200:
            allpage.append(url)
            url = ''.join([fenlei, page_pre, str(next),'.html'])
            next += 1
        else:
            break
    return allpage

def get_allpics_url_fenlei(fenlei_url):
    allpage = get_fenlei_allpage(fenlei_url)
    allpersons = map(get_page_all_person,allpage)
    allpersons = reduce(lambda x,y:x + y,allpersons)
    allpics = map(get_person_pic_url_Set,allpersons)
    allpics = reduce(lambda x,y:x + y,allpics)
    return allpics

    
if __name__ == '__main__':
    print 'start to run crawler\n'
    fenlei_url = get_fenlei_url(main_url)
    allpics = get_allpics_url_fenlei(fenlei_url[0])
    pool = ThreadPool(10)
    pool.map(dowload_pic,allpics)
    pool.close()
    pool.join()
  
