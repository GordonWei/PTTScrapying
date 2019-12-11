#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Author : GordonWei
#Date : 11/28/18
#Blog : https://www.kmp.tw/
#comment : Scrapying ptt.cc MacShop and find Apple Watch DEMO

import requests, re, time, lineTool
from bs4 import BeautifulSoup

todayMonth = time.strftime('%m')
todayMonth = int(todayMonth)
if todayMonth - 1 < 9 :
        todayMonth = ' ' + str(todayMonth)
else:
        todayMonth = str(todayMonth)

todayDay = time.strftime('%d')
today = todayMonth + '/' + todayDay
lineToken = '<Your Line Notify Token>'
ptt_site = 'https://www.ptt.cc/bbs/MacShop/index.html'
indexRes = requests.get(ptt_site)
indexSoup = BeautifulSoup(indexRes.text, 'html.parser')
pages = indexSoup.find_all('a', text = re.compile('上頁'))
pages = str(pages)
a = pages.replace('[<a class="btn wide" href="/bbs/MacShop/index' , '')
b = a.replace( '.html">‹ 上頁</a>]', '')
b = int(b)
c = b - 2

for p in range(b+1, c, -1 ):
        url = 'https://www.ptt.cc/bbs/MacShop/index' + str(p) + '.html'
        res = requests.get(url)
        if res.status_code == requests.codes.ok:
                soup = BeautifulSoup(res.text, 'html.parser')
                stories = soup.find_all('div', class_ = 'r-ent')
                for s in stories:
                        if s.find('div', 'date').string == today and s.find('a', text = re.compile(r'[販售](.*)watch(.*)', re.I)):
                                if s.find('a'):
                                        href = s.find('a')['href']
                                        title = s.find('a').text
                                        date = s.find('div','date').text
                                print('https://www.ptt.cc' + href, title, date)
                                botText = ('https://www.ptt.cc' + href + '\n' + title, date)
                                lineTool.lineNotify(lineToken, botText)
