
# coding: UTF-8
# -*- coding:utf-8 -*-
# 中文注释
#导入各种包 大家自行百度作用
import re   #正则表达式
import threading    #线程
import os       #常用函数库
from urllib2 import Request,urlopen,URLError,HTTPError  #url 库
from lxml import etree          #解析库

#定义myTread类
class myThread (threading.Thread):   #继承父类threading.Thread
    def __init__(self, url, newdir,CrawledURLs):#构造函数
        threading.Thread.__init__(self)
        self.url = url
        self.newdir = newdir
        self.CrawledURLs=CrawledURLs
    def run(self):                   #把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        CrawListPage(self.url, self.newdir,self.CrawledURLs)
#初始访问地址
starturl="http://www.ygdy8.com/index.html"
#host设置
host="http://www.ygdy8.com"
#判断地址是否已经爬取
def __isexit(newurl,CrawledURLs):#时间复杂度O(n)，这一块有待提高
    for url in CrawledURLs:
        if url == newurl:
            return True
    return False

#获取页面资源
def __getpage(url):
    req = Request(url)
    #设置访问代理
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 ' \
                 '(KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
    #添加头
    req.add_header('User-Agent', user_agent)
    try:
        response = urlopen(req, timeout=60)#设置访问时长一分钟
    except:
        return "error"
        pass
    else:
        page = response.read()
        return page
#处理资源页面 爬取资源地址
def CrawlSourcePage(url,filedir,filename,CrawledURLs):
    print url
    page = __getpage(url)
    if page=="error":
        return
    CrawledURLs.append(url)
    page = page.decode('gbk', 'ignore')#GBK一定要加 注意编码
    tree = etree.HTML(page)
    Nodes = tree.xpath("//div[@align='left']//table//a")#使用re正则表达获取节点
    #构造生成文件参数
    try:
        source = filedir + "/" + filename + ".txt"
        f = open(source.decode("utf-8"), 'w')
        for node in Nodes:
            sourceurl = node.xpath("text()")[0]
            f.write(sourceurl.encode("utf-8")+"\n")
        f.close()
    except:
        print "生成文件过程出错！"

# 解析分类文件
def CrawListPage(indexurl,filedir,CrawledURLs):
    print "正在解析分类主页资源"
    print indexurl
    page = __getpage(indexurl)
    if page=="error":
        return
    CrawledURLs.append(indexurl)
    page = page.decode('gbk', 'ignore')
    tree = etree.HTML(page)
    Nodes = tree.xpath("//div[@class='co_content8']//a")
    for node in Nodes:
        url=node.xpath("@href")[0]
        if re.match(r'/', url):
            # 非分页地址 可以从中解析出视频资源地址
            if __isexit(host + url,CrawledURLs):
                pass
            else:
                #文件命名是不能出现以下特殊符号
                filename=node.xpath("text()")[0].encode("utf-8").replace("/"," ")\
                                                                .replace("\\"," ")\
                                                                .replace(":"," ")\
                                                                .replace("*"," ")\
                                                                .replace("?"," ")\
                                                                .replace("\""," ")\
                                                                .replace("<", " ") \
                                                                .replace(">", " ")\
                                                                .replace("|", " ")
                CrawlSourcePage(host + url,filedir,filename,CrawledURLs)
            pass
        else:
            # 分页地址 从中嵌套再次解析
            print "分页地址 从中嵌套再次解析",url
            index = indexurl.rfind("/")
            baseurl = indexurl[0:index + 1]#取到/为止
            pageurl = baseurl + url
            if __isexit(pageurl,CrawledURLs):
                pass
            else:
                print "分页地址 从中嵌套再次解析", pageurl
                CrawListPage(pageurl,filedir,CrawledURLs)
            pass
    pass

#解析首页
def CrawIndexPage(starturl):
    print "正在爬取首页"
    page = __getpage(starturl)
    if page=="error":
        return
    page = page.decode('gbk', 'ignore')
    tree = etree.HTML(page)
    Nodes = tree.xpath("//div[@id='menu']//a")
    print "首页解析出地址",len(Nodes),"条"
    for node in Nodes:
        CrawledURLs = []
        CrawledURLs.append(starturl)
        url=node.xpath("@href")[0]
        if re.match(r'/html/[A-Za-z0-9_/]+/index.html', url):
            if __isexit(host + url,CrawledURLs):
                pass
            else:
                try:
                    catalog = node.xpath("text()")[0].encode("utf-8")
                    newdir = "C:/电影资源/" + catalog

                    os.makedirs(newdir.decode("utf-8"))
                    print "创建分类目录成功------"+newdir
                    thread = myThread(host + url, newdir,CrawledURLs)
                    thread.start()
                except:
                    pass
CrawIndexPage(starturl)