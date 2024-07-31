#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytz
import requests
import m3u8
import sys
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib.parse import urlparse, urljoin
import strict_rfc3339
import re
from datetime import datetime


# 获取中国时区
china_tz = pytz.timezone('Asia/Shanghai')

sourceIcon51ZMT="http://epg.51zmt.top:8000"
sourceChengduMulticast="http://epg.51zmt.top:8000/sctvmulticast.html"
# homeLanAddress="http://192.168.100.22:4022"
homeLanAddress="http://192.168.100.2:7088"


# groupCCTV=["CCTV", "CETV", "CGTN"]
groupCCTV=["CCTV"]
groupWS=[ "卫视"]
groupSC=["SCTV", "四川", "CDTV", "熊猫", "峨眉", "成都"]
listUnused=["单音轨", "画中画", "热门", "直播室", "爱", "92"]

orders=["CCTV", "卫视", "四川", "其他"]


index = 1
def getID():
    global index
    index = index+1
    return index-1

def setID(i):
    global index
    if i > index:
        index = i+1
    return index

def checkChannelExist(listIptv, channel):
    for k, v in listIptv.items():
        if isIn(k, channel):
            return True
    return False

def isIn(items, v):
    for item in items:
        if item in v:   # 字符串内检查是否有子字符串
            return True

def filterCategory(v):
    if isIn(groupCCTV, v):
        return "CCTV"
    elif isIn(groupWS, v):
        return "卫视"
    elif isIn(groupSC, v):
        return "四川"
    else:
        return "其他"

def findIcon(m, id):
    for v in m:
        if v["name"] == id:
            return urljoin(sourceIcon51ZMT, v["icon"])
            #return 'http://epg.51zmt.top:8000/' + v["icon"]

    return ""


def loadIcon():
    res = requests.get(sourceIcon51ZMT).content
    m=[]
    #res=""
    #with open('./index.html') as f:
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

def generateM3U8(file):
    file=open(file, "w")
    name = '成都电信IPTV - ' + strict_rfc3339.now_to_rfc3339_utcoffset()
    title = '#EXTM3U name=\"' + name + '\"' + ' url-tvg=\"http://epg.51zmt.top:8000/e.xml\"\n\n'
    file.write(title)
    for group in orders:
        k=group
        v=m[group]
        for c in v:
            if "dup" in c:
                continue

            line = '#EXTINF:-1 tvg-logo="%s" tvg-id="%s" catchup="default" catchup-source="%s?playseek={utc:YmdHMS}-{utcend:YmdHMS}" tvg-name="%s" group-title="%s",%s\n' % (c["icon"], c["id"], c["catchupSource"], c["name"], k, c["name"])
            line2 = homeLanAddress + '/udp/' + c["address"] + "\n"
            # line2 = c["catchupSource"] + "\n"

            file.write(line)
            file.write(line2)

    file.close()
    print("Build m3u8 success.")
    
def convertM3U8(file, new_file):
    url = 'http://epg.51zmt.top:8000/api/upload/'
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Origin': 'http://epg.51zmt.top:8000',
        'Pragma': 'no-cache',
        'Referer': 'http://epg.51zmt.top:8000/',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }
    files = {
        'myfile': ('iptv.m3u8', open(file, 'rb'), 'audio/mpegurl')
    }
    
    response = requests.post(url, headers=headers, files=files, verify=False)
    print(response.text)
    # 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    # 在HTML中查找下载链接
    download_link = soup.find('a', href=True)
    if download_link:
        file_url = download_link['href']
        # 获取绝对URL
        absolute_url = urljoin(urlparse(url).scheme + "://" + urlparse(url).hostname, file_url)
        # 下载文件
        file_response = requests.get(absolute_url)
        # 将'your_file_name.extension'替换为所需的文件名和扩展名
        with open(new_file, 'wb') as file:
            file.write(file_response.content)
        print('文件成功下载！')
        # 打开文件并读取内容
        with open(new_file, 'r') as file:
            lines = file.readlines()
        # 替换第一行内容
        if lines:
            # 获取当前时间
            now = datetime.now(china_tz)
            name = '成都电信IPTV - ' + now.strftime("%Y-%m-%d %H:%M:%S")
            title = '#EXTM3U name=\"' + name + '\"' + ' url-tvg=\"http://epg.51zmt.top:8000/e.xml\"\n'
            lines[0] = title
            # lines[0] = '#EXTM3U name="成都电信IPTV - 2024-01-15T03:08:35Z" url-tvg="http://epg.51zmt.top:8000/e.xml"\n'
        # 将修改后的内容写回文件
        with open(new_file, 'w') as file:
            file.writelines(lines)
        print('第一行内容已成功替换！')
    else:
        print('在页面上找不到下载链接。')


def generateTXT(file):
    file=open(file, "w")
    for k, v in m.items():
        line = '%s,#genre#\n' % (k)
        file.write(line)

        for c in v:
            line = '%s,%s/udp/%s\n' % (c["name"], homeLanAddress, c["address"])
            if "ct" not in c:
                line = '%s,%s\n' % (c["name"], c["address"])

            file.write(line)

    file.close()
    print("Build txt success.")


def generateHome():
    generateM3U8("./home/iptv_org.m3u8")
    print("生成m3u8成功")
    convertM3U8("./home/iptv_org.m3u8", "./home/iptv.m3u8")
    print("转换m3u8成功")
    # generateTXT("./home/iptv.txt")

#exit(0)


mIcons = loadIcon()
print("台标加载完成")

res = requests.get(sourceChengduMulticast).content
soup = BeautifulSoup(res, 'lxml')
m={}
for tr in soup.find_all(name='tr'):
    td = tr.find_all(name='td')
    if td[0].string == "序号":
        continue

    name = td[1].string
    if isIn(listUnused, name):
        continue

    setID(int(td[0].string))

    name = name.replace('超高清', '').replace('高清', '').replace('-', '').strip()

    group = filterCategory(name)
    icon = findIcon(mIcons, name)

    if group not in m:
        m[group] = []

    m[group].append({"id": td[0].string, "name": name, "address": td[2].string, "catchupSource": td[6].string, "icon": icon})
print("频道加载完成")
generateHome()