#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytz
import requests, os
from bs4 import BeautifulSoup,Comment
from urllib.parse import urlparse, urljoin
from datetime import datetime
import fill_m3u8, fill_erw_epg

groupCCTV = ["CCTV"]
groupWS = ["卫视"]
groupSC = ["SCTV", "四川", "CDTV", "熊猫", "峨眉", "成都"]
# 过滤如下列表中的频道
listUnused = ["单音轨", "画中画", "热门", "直播室", "爱", "92", "创新及人才", "云演艺", "雅克音乐", "电信导视", "嘉佳卡通", "家政频道", "戏曲专区", "生活时尚", "足球高清专区", "红色影院专区", "经典剧场专区", "解密高清专区", "地理高清专区", "导视专区", "来钓鱼", "麻辣体育", "绚影", "亲子趣学", "中录动漫", "中国体育"]

orders = ["CCTV", "卫视", "四川", "其他"]

def loadIcon():
    res = requests.get("http://epg.51zmt.top:8000", timeout=(10, 30)).content
    m = []
    # res=""
    # with open('./index.html') as f:
    #    res=f.read()

    soup = BeautifulSoup(res, 'lxml')

    for tr in soup.find_all('tr'):
        td = tr.find_all('td')
        if len(td) < 4:
            continue

        href = ""
        for a in td[0].find_all('a', href=True):
            if a["href"] == "#":
                continue
            href = a["href"]

        if href != "":
            m.append({"id": td[3].string, "name": td[2].string, "icon": href})

    return m

def isIn(items, v):
    for item in items:
        if item in v:  # 字符串内检查是否有子字符串
            return True

def findIcon(m, id):
    if id == "CCTV少儿":
        return "http://epg.51zmt.top:8000/tb1/CCTV/CCTV14.png"
    for v in m:
        if v["name"] == id:
            return urljoin('http://epg.51zmt.top:8000/', v["icon"])
            # return 'http://epg.51zmt.top:8000/' + v["icon"]
    res = requests.get("https://epg.erw.cc", timeout=(10, 30)).content
    soup = BeautifulSoup(res, 'lxml')
    tag = soup.find(string=id)
    if tag:
        parent = tag.parent.parent
        comments = parent.find_all(string=lambda text: isinstance(text, Comment))
        # 遍历所有注释，查找其中包含的 <a> 标签
        for comment in comments:
            comment_soup = BeautifulSoup(comment, 'html.parser')
            link = comment_soup.find('a')
            if link and link.has_attr('href'):
                href = link['href']
                return href
    return ""

def main():
    print("开始加载台标")
    mIcons = loadIcon()
    print("台标加载完成")
    print("开始加载频道")
    res = requests.get("http://epg.51zmt.top:8000/sctvmulticast.html", timeout=(10, 30)).content
    soup = BeautifulSoup(res, 'lxml')
    m = {}
    for tr in soup.find_all(name='tr'):
        td = tr.find_all(name='td')
        if td[0].string == "序号":
            continue
        if td[5].string == '未能播放':
            continue
        name = td[1].string
        if isIn(listUnused, name):
            continue

        name = fill_m3u8.fullwidth_to_halfwidth(name)
        name = name.replace('超高清', '').replace('高清', '').replace('-', '').strip()
        if name == 'CCTV少儿':
            name = 'CCTV14'
        iconUrl = findIcon(mIcons, name)
        print(f'{name} --  {iconUrl}')
        chunk_download(iconUrl, name)


def chunk_download(url, filename):
    if url:
        f_name=f'../logo/{filename}.png'
        if not os.path.exists(f_name):
            # a = urlparse(url)
            # file_name = os.path.basename(a.path)
            # _,file_suffix = os.path.splitext(file_name)
            r = requests.get(url, stream=True)
            with open(f'../logo/{filename}.png', 'wb') as f:
                for chunk in r.iter_content(chunk_size=32):
                    f.write(chunk)


# iconUrl = findIcon([], "四川乡村")

main()
