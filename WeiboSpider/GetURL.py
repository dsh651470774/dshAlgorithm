# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import datetime
import pandas as pd
import urllib
import csv

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
           'Host': 's.weibo.com',
           #"Cookie": "_T_WM=0364d138c74acfd49fcf1f927f0bb479;WEIBOCN_WM=3349;H5_wentry=H5;backURL=http%3A%2F%2Fweibo.cn%2F%3Fretcode%3D6102;SCF=Ao0ALZrVxtpgvQuuSDSk_lk2B4F61CQVuElGMtxFGe0sptYR8NVy3SorfK3WWbtBijgAStvmxUnApg-CkiqgDNY.;SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhnqG4XiuKXOlmqy3E41hk15JpX5K-hUgL.FoeRS0BceKz41hn2dJLoIpMLxK-LBK-L1hnLxKqL1KqLB-9keK.RSntt;SUB=_2A2502Y7ZDeRhGeVG7FYX8SzFwzSIHXVUJRKRrDV6PUJbkdBeLXTbkW0Ku5okXYALyvdvIJpPLCxiK_FF6g..;SUHB=0nluUCn8oqrwLA;SSOLoginState=1507720841;H5:PWA:UID=1;M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D100803"
           "Cookie": "SINAGLOBAL=1981277765990.1282.1507634517668; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhnqG4XiuKXOlmqy3E41hk15JpX5KMhUgL.FoeRS0BceKz41hn2dJLoIpMLxK-LBK-L1hnLxKqL1KqLB-9keK.RSntt; wvr=6; UOR=,,login.sina.com.cn; ALF=1545892587; SSOLoginState=1514356588; SCF=Ao0ALZrVxtpgvQuuSDSk_lk2B4F61CQVuElGMtxFGe0simacg-zUDlpTtesuueaAjQn1mgZkhDBose4Wr7wgML0.; SUB=_2A253R088DeRhGeVG7FYX8SzFwzSIHXVUNSf0rDV8PUNbmtBeLVHCkW9NT4DLpnB6s00_cW-7DTDBnASa6D0m4Q1C; SUHB=0nluUCn8opVtSR; _s_tentry=login.sina.com.cn; Apache=9105320497055.395.1514356591994; ULV=1514356592014:7:3:2:9105320497055.395.1514356591994:1514199571970; SWBSSL=usrmdinst_16; SWB=usrmdinst_14"
           }

class url():
    def __init__(self,keyword,province,start,end):
        self.keyword=keyword
        self.province=province
        self.starttime=start
        self.endtime=end
        self.provincecode=pd.read_csv('china.csv')
        self.findprovince()
        [self.citycode,self.cityname]=self.findprovince()
        self.timelist=self.gettimeList()
        [self.urllist,self.procity]=self.buildrl()

    def findprovince(self):
        selectprovince=self.provincecode[self.provincecode['province'] == self.province]
        citycode=[]
        cityname=[]
        if self.province == '北京市' or self.province == '天津市' or self.province == '上海市' or self.province == '重庆市':
            citynum=''
            for item in selectprovince.iterrows():
                citynum=str(item[1]['number'])
                cityname.append(item[1]['city'])
                citycode.append(citynum[0:2]+':'+citynum[4:6])
            cityname.append('全部')
            citycode.append(citynum[0:2] + ':' + '1000')
        else:
            citynum = ''
            for item in selectprovince.iterrows():
                citynum = str(item[1]['number'])
                cityname.append(item[1]['city'])
                citycode.append(citynum[0:2] + ':' + citynum[2:4])
            cityname.append('全部')
            citycode.append(citynum[0:2] + ':' + '1000')
        return citycode ,cityname

    def gettimeList(self):
        self.starttime=datetime.datetime.strptime(self.starttime, '%Y-%m-%d-%H')
        self.endtime = datetime.datetime.strptime(self.endtime, '%Y-%m-%d-%H')
        urllist = []
        urllist=[]
        temp=self.starttime
        onehour=datetime.timedelta(hours=1)
        while temp<self.endtime:
            temp2=temp+onehour
            urllist.append(temp.strftime('%Y-%m-%d-%H')  +':'+temp2.strftime('%Y-%m-%d-%H'))
            temp=temp2
        return urllist

    def buildrl(self):
        urllist = []
        procity=[]
        for i in range(0,self.citycode.__len__()):
            for j in range(0,self.timelist.__len__()):
                strurl = 'http://s.weibo.com/weibo/'
                once = urllib.urlencode({"kw": self.keyword})[3:]
                one_keywords = urllib.urlencode({"kw": once})[3:]
                strurl = strurl + one_keywords
                strurl=strurl+'&region=custom:'+self.citycode[i]+'&typeall=1&suball=1&timescope=custom:'+self.timelist[j]
                urllist.append(strurl)
                procity.append(self.province+self.cityname[i])
        return urllist,procity


u = url('台风', '广东省', '2017-08-22-00', '2017-08-24-00')
with open("urllist.csv", "wb") as csvfile:
    writer = csv.writer(csvfile)
    # 先写入columns_name
    writer.writerow(["num", "cityname", "url"])
    for i in range(0, len(u.urllist)):
        cityname = u.procity[i].decode('utf8').encode('GB18030', 'ignore')
        writer.writerow([i + 1, cityname, u.urllist[i]])
