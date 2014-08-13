#-*-coding:utf-8-*-
import os,sys
import re
import urllib
import threading
import Queue
from BeautifulSoup import BeautifulSoup
import requests
from multiprocessing.pool import ThreadPool
from multiprocessing import Pool,Queue,Process

main_url = 'http://www.22mm.cc'
page_pre = 'index_'
save_path = '/root/Desktop/picture2/'

proxylist = (
            '211.167.112.14:80',
            '115.47.8.39:80',
            )

def getSoup(url,proxylist=proxylist):
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

def get_pic_url(url):
    soup = getSoup(url)
    result = soup.findAll('script')
    mm = result[6].getString
    cc = str(mm).split('"')[-2]
    cc = cc.replace('big','pic')
    return cc

#download one pic
def download_pic(url,path=save_path):
    r = requests.get(url)
    path = path + str(url).split('/')[-1]
    urllib.urlretrieve(url,path)

#get person from page    
def get_page_all_person(page,main_url=main_url):
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

def get_person_pic_url_Set(person_url):
    pool = ThreadPool(8)
    soup = getSoup(person_url)
    tag = soup.find('div',{'class':'pagelist'}).findAll('a')
    result = [i.get('href') for i in tag]
    pre = '/'.join(person_url.split('/')[:-1]) + '/'
    g = lambda x:pre + x
    result = map(g,result)
    result[0] = person_url
    result.pop()
    result = pool.map(get_pic_url,result)
    pool.close()
    pool.join()
    return result
    
def dowload_person(person_url):
    print 'start to downlaod person %s\n'%(person_url)
    person_pic_url = get_person_pic_url_Set(person_url)
    pool = ThreadPool(8)
    pool.map(download_pic,person_pic_url)
    pool.close()
    pool.join()

def download_from_page(page_url):
    page_persons = get_page_all_person(page_url)
    pool = ThreadPool(7)
    pool.map(dowload_person,page_persons)
    pool.close()
    pool.join()

def download_allpage(fenlei,page_pre = page_pre):
    url = fenlei
    next = 2
    while True:
        r = requests.get(url)
        if r.status_code == 200:
            download_from_page(url)
            url = ''.join([fenlei, page_pre, str(next),'.html'])
            next += 1
        else:
            break
        
    
if __name__ == '__main__':
    fenlei_url = get_fenlei_url(main_url)
    map(download_allpage,fenlei_url)
    print '\nfinish the download\n'
