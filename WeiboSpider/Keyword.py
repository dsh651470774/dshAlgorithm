# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import time
import urllib2
import pandas as pd
import xlwt
import random
import csv

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
           'Host': 's.weibo.com',
           #"Cookie": "_T_WM=0364d138c74acfd49fcf1f927f0bb479;WEIBOCN_WM=3349;H5_wentry=H5;backURL=http%3A%2F%2Fweibo.cn%2F%3Fretcode%3D6102;SCF=Ao0ALZrVxtpgvQuuSDSk_lk2B4F61CQVuElGMtxFGe0sptYR8NVy3SorfK3WWbtBijgAStvmxUnApg-CkiqgDNY.;SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhnqG4XiuKXOlmqy3E41hk15JpX5K-hUgL.FoeRS0BceKz41hn2dJLoIpMLxK-LBK-L1hnLxKqL1KqLB-9keK.RSntt;SUB=_2A2502Y7ZDeRhGeVG7FYX8SzFwzSIHXVUJRKRrDV6PUJbkdBeLXTbkW0Ku5okXYALyvdvIJpPLCxiK_FF6g..;SUHB=0nluUCn8oqrwLA;SSOLoginState=1507720841;H5:PWA:UID=1;M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D100803"
           "Cookie": 'login_sid_t=3b50f908b55083c43155566e50cd5ce1; cross_origin_proto=SSL; _s_tentry=passport.weibo.com; Apache=3153387107021.2993.1514529340861; SINAGLOBAL=3153387107021.2993.1514529340861; ULV=1514529340871:1:1:1:3153387107021.2993.1514529340861:; SWBSSL=usrmdinst_15; SWB=usrmdinst_11; WBStorage=c1cc464166ad44dc|undefined; crossidccode=CODE-gz-1EuOLH-15KOS6-wpicbRYTRMDejkse0519c; ALF=1546067286; SSOLoginState=1514531286; SUB=_2A253QZmHDeThGeNI61AU9ifOyTSIHXVUNoxPrDV8PUNbmtBeLUbckW9NSI1mvoJQPWAoDhA3zNq8m-yAuZanFtat; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5non7BiV3N_uXS.4HTIedX5JpX5KzhUgL.Fo-cehzfSo.Eeon2dJLoIE5LxKnL1K2LBKeLxKBLBonL1KqLxKqLBo-LBoMRSoqXeBtt; SUHB=0wnlkdptFulhYJ; wvr=6; UOR=,,graph.qq.com'
           }

def readurllist(strFile):
    df=pd.read_csv(strFile)
    urllist=[]
    citylist=[]
    for i in range(0,df.__len__()):
        urllist.append(df.iloc[i]['url'])
        citylist.append(df.iloc[i]['cityname'])
    return urllist,citylist

def download(urllist,citylist):
    rowNum = 0
    urlNum = 1
    with open("Weibodata.csv", "wb") as csvfile:
        writer2 = csv.writer(csvfile)
        for urlCount in range(0,len(urllist)):
            hasMore = True  # 某次请求可能少于50页，设置标记，判断是否还有下一页
            isCaught = False  # 某次请求被认为是机器人，设置标记，判断是否被抓住。抓住后，需要，进入页面，输入验证码
            name_filter = set([])  # 过滤重复的微博ID
            i = 1  # 记录本次请求所返回的页数
            while hasMore and i < 51 and (not isCaught):  # 最多返回50页，对每页进行解析，并写入结果文件
                strurl = urllist[urlCount] + '&page=' + str(i)
                data = ''  # 存储该页的网页数据
                goon = True  # 网络中断标记
                ##网络不好的情况，试着尝试请求三次
                for tryNum in range(0, 3):
                    try:
                        req = urllib2.Request(strurl, headers=HEADERS)
                        data = urllib2.urlopen(req,timeout=12).read()
                        break
                    except:
                        if tryNum < 2:
                            time.sleep(10)
                        else:
                            print 'Internet Connect Error!'
                            goon = False
                            break
                if goon:
                    lines = data.splitlines()
                    isCaught = True
                    for line in lines:
                        ## 判断是否有微博内容，出现这一行，则说明没有被认为是机器人
                        if line.startswith('<script>STK && STK.pageletM && STK.pageletM.view({"pid":"pl_weibo_direct"'):
                            isCaught = False
                            n = line.find('html":"')
                            if n > 0:
                                j = line[n + 7: -12].encode("utf-8").decode('unicode_escape').encode("utf-8").replace("\\",
                                                                                                                      "")  # 去掉所有的\
                                ## 没有更多结果页面
                                if (j.find('<div class="search_noresult">') > 0):
                                    hasMore = False
                                    break
                                ## 有结果的页面
                                else:
                                    soup = BeautifulSoup(j, "html.parser")
                                    # 获取昵称和微博内容
                                    cityname = citylist[urlCount]
                                    div = soup.findAll('div', attrs={"class": "WB_cardwrap S_bg2 clearfix"})
                                    for item in div:
                                        passtime = item.find('a',
                                                         attrs={"class": "W_textb", "node-type": "feed_list_item_date"}).text.replace('\n','').replace('\t','')
                                        user = item.find('a', attrs={"class": "name_txt W_fb"}).text.replace('\n','').replace('\t','')
                                        content = item.find('p', attrs={"class": "comment_txt"}).text.replace('\n','').replace('\t','')
                                        writer2.writerow([rowNum + 1, passtime.encode('GB18030','ignore'), cityname,user.encode('GB18030','ignore'),content.encode('GB18030','ignore')])
                                        rowNum = rowNum + 1
                                        print '已搜索第%d条' % rowNum
                print '已搜索第%d页' % i
                i=i+1
                timesleep = random.randrange(20, 40)
                time.sleep(timesleep)
            if isCaught:
                print('Error Catugted!')
                break

            print '第%d条url已经搜索完成'%urlNum
            urlNum=urlNum+1
        print '已经全部搜索完毕！'

[urllist,citylist]=readurllist('urllist.csv')
download(urllist,citylist)


