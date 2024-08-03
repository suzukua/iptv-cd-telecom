#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytz
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from datetime import datetime
import fill_m3u8

# 获取中国时区
china_tz = pytz.timezone('Asia/Shanghai')

sourceIcon51ZMT = "http://epg.51zmt.top:8000"
sourceChengduMulticast = "http://epg.51zmt.top:8000/sctvmulticast.html"
# homeLanAddress="http://192.168.100.22:4022"
homeLanAddress = "http://192.168.100.2:7088"

# groupCCTV=["CCTV", "CETV", "CGTN"]
groupCCTV = ["CCTV"]
groupWS = ["卫视"]
groupSC = ["SCTV", "四川", "CDTV", "熊猫", "峨眉", "成都"]
listUnused = ["单音轨", "画中画", "热门", "直播室", "爱", "92"]

orders = ["CCTV", "卫视", "四川", "其他"]

index = 1


def getID():
    global index
    index = index + 1
    return index - 1


def setID(i):
    global index
    if i > index:
        index = i + 1
    return index


def checkChannelExist(listIptv, channel):
    for k, v in listIptv.items():
        if isIn(k, channel):
            return True
    return False


def isIn(items, v):
    for item in items:
        if item in v:  # 字符串内检查是否有子字符串
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
            # return 'http://epg.51zmt.top:8000/' + v["icon"]

    return ""


def loadIcon():
    res = requests.get(sourceIcon51ZMT).content
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


def generateM3U8(file):
    file = open(file, "w", encoding='utf-8')
    name = '成都电信IPTV - ' + datetime.now(china_tz).strftime("%Y-%m-%d %H:%M:%S")
    title = f'#EXTM3U name="{name}"' + ' x-tvg-url="https://epg.erw.cc/all.xml.gz" url-tvg="http://epg.51zmt.top:8000/e.xml.gz"\n\n'
    file.write(title)
    for group in orders:
        k = group
        v = m[group]
        for c in v:
            if "dup" in c:
                continue
            line = '#KODIPROP:inputstream=inputstream.ffmpegdirect\n#EXTINF:-1 tvg-logo="%s" tvg-id="%s" catchup="append" catchup-days="%s" catchup-source="?playseek={utc:YmdHMS}-{utcend:YmdHMS}" tvg-name="%s" group-title="%s",%s\n' % (
            c["icon"], c["id"], c["catchupDays"], c["name"], k, c["name"])
#             line2 = homeLanAddress + '/udp/' + c["address"] + "\n"
            line2 = c["catchupSource"] + "\n"

            file.write(line)
            file.write(line2)
    file.close()
    print("Build m3u8 success.")


def upload_convert_egp(m3u8_file, epg_m3u8_file):
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
        'myfile': ('iptv.m3u8', open(m3u8_file, 'rb'), 'audio/mpegurl')
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
        with open(epg_m3u8_file, 'w', encoding='utf-8') as file:
            file.write(file_response.content.decode())
        print('文件成功下载！')
    else:
        print('在页面上找不到下载链接。')


def generateHome():
    m3u8_file = './home/iptv.m3u8'
    epg_m3u8_file = './home/iptv_epg.m3u8'
    generateM3U8(m3u8_file)
    print("生成m3u8完成")
    upload_convert_egp(m3u8_file, epg_m3u8_file)
    print("补齐egp文件完成")
    fill_m3u8.fill_config(epg_m3u8_file, m3u8_file)
    print("修正m3u8文件完成")


# exit(0)


mIcons = loadIcon()
print("台标加载完成")

res = requests.get(sourceChengduMulticast).content
soup = BeautifulSoup(res, 'lxml')
m = {}
for tr in soup.find_all(name='tr'):
    td = tr.find_all(name='td')
    if td[0].string == "序号":
        continue

    name = td[1].string
    if isIn(listUnused, name):
        continue

    setID(int(td[0].string))

    name = fill_m3u8.fullwidth_to_halfwidth(name)
    name = name.replace('超高清', '').replace('高清', '').replace('-', '').strip()

    group = filterCategory(name)
    icon = findIcon(mIcons, name)

    if group not in m:
        m[group] = []

    m[group].append({"id": td[0].string, "name": name, "address": td[2].string, "catchupSource": td[6].string,
                     "catchupDays": td[3].string, "icon": icon})
print("频道加载完成")
generateHome()
