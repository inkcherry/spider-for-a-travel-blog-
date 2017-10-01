#coding:utf8
import urllib2
import re
import urlparse
import cookielib
from bs4 import BeautifulSoup
def download(url):  
    i_headers = {"User_agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1"}
    if url is None:
    	return
    request = urllib2.Request(url,i_headers)
    response = urllib2.urlopen(url)
    if response.getcode()!=200:
        return 
    initial_html=response.read()
    clean_html=''.join(re.split(r"<\!–\[if lte IE 6\]>|<\!\[endif\]–>", initial_html))  
    return clean_html

def output():  
	pass

def pageselect(tag): #自定义的find函数
    check_classes=['SG_pgon','SG_pgnext']
    if(tag.has_attr('class')):
        for class_ in tag.get('class'):
            for check_class in check_classes:
                if class_==check_class:
                    return False
        

    return tag.name=='li'
def getpageurl(page_url,): #获取页面信息
    soup = BeautifulSoup(open('output.html'), 'html.parser', from_encoding='utf-8')
  
    lis=soup.find('ul',class_='SG_pages').find_all(pageselect)
    for li in lis:
        page_url.append(li.find('a')['href'])

def urlmanager(page_url,root_content,urls,titles):   
    getpageurl(page_url)    #获取所有的页面url 其中root_url为第一页的内容
    curr_content=root_content
    count_=-1
    len_page=len(page_url)
    while True:
        soup = BeautifulSoup(curr_content, 'html.parser', from_encoding='utf-8')
        spans=soup.find_all('span',class_="atc_title")
        for span in spans:
            link= span.find('a')
            urls.append(link['href'])
            titles.append(link.get_text().replace(':','：'))
        count_=count_+1
        if count_==len_page:
            break
        curr_content=download(page_url[count_]) #遍历所有页面


	# return urls
def gettext(urls,texts,titles): #从所有url里面获取文章内容
    count_=0
    print len(urls)


    for i in range(0,len(urls)):
        soup=BeautifulSoup(download(urls[i]),'html.parser',from_encoding='utf-8')
        textdiv=soup.find('div',id='sina_keyword_ad_area2')
        texts.append(textdiv.get_text())
        print "已经爬取第%s篇文章" % count_
        filesrc=['travel\\',titles[i],'.txt']
        fout=open(str(i).join(filesrc),"w+")
        fout.write('%s'% texts[i])
        fout.close()


if __name__ == '__main__':
    url=[]
    titles=[]
    texts=[]
    page_url=[]
    root_url="http://blog.sina.com.cn/s/articlelist_1776757314_0_1.html"

    root_content=download(root_url)

    urlmanager(page_url,root_content,url,titles)
    gettext(url,texts,titles)
    # output(titles,text,url)
    # fout=open("text1test.html","w+")
   

