#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytz,os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from datetime import datetime
import fill_m3u8, fill_erw_epg

# 获取中国时区
china_tz = pytz.timezone('Asia/Shanghai')

sourceIcon51ZMT = "https://epg.51zmt.top:8001"
sourceChengduMulticast = "https://epg.51zmt.top:8001/sctvmulticast.html"
homeLanAddress = "http://192.168.100.1:4022"

# groupCCTV=["CCTV", "CETV", "CGTN"]
groupCCTV = ["CCTV"]
groupWS = ["卫视"]
groupSC = ["SCTV", "四川", "CDTV", "熊猫", "峨眉", "成都"]
# 过滤如下列表中的频道
listUnused = ["单音轨", "画中画", "热门", "直播室", "爱", "92", "创新及人才", "云演艺", "雅克音乐", "电信导视", "嘉佳卡通", "家政频道",
              "戏曲专区", "生活时尚", "足球高清专区", "红色影院专区", "经典剧场专区", "解密高清专区", "地理高清专区", "导视专区", "来钓鱼",
              "麻辣体育", "绚影", "亲子趣学", "中录动漫", "中国体育", "健康养生", "SCTV-6", "CETV-4"]

orders = ["CCTV", "卫视", "四川", "其他"]




def isIn(items, v):
    for item in items:
        if item in v:  # 字符串内检查是否有子字符串
            return True


def filterCategory(v):
    if isIn(groupCCTV, v):
        return orders[0]
    elif isIn(groupWS, v):
        return orders[1]
    elif isIn(groupSC, v):
        return orders[2]
    else:
        return orders[3]


def findIcon(m, id):
    for v in m:
        if v["name"] == id:
            return urljoin(sourceIcon51ZMT, v["icon"])
            # return 'http://epg.51zmt.top:8000/' + v["icon"]

    return ""


def loadIcon():
    res = requests.get(sourceIcon51ZMT, verify=False, timeout=(10, 60)).content
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
    # title = f'#EXTM3U name="{name}"' + ' x-tvg-url="https://epg.erw.cc/all.xml.gz" url-tvg="http://epg.51zmt.top:8000/e.xml.gz"\n'
    # title = f'#EXTM3U name="{name}"' + ' x-tvg-url="https://epg.erw.cc/all.xml.gz"\n'
    title = f'#EXTM3U name="{name}"' + ' x-tvg-url="https://epg.zsdc.eu.org/t.xml.gz"\n'
    file.write(title)
    for group in orders:
        v = [iptv for iptv in iptvList if iptv["group"] == group]
        for c in v:
            if "dup" in c:
                continue
            line = '#KODIPROP:inputstream=inputstream.ffmpegdirect\n#EXTINF:-1 tvg-logo="%s" tvg-id="%s" tvg-name="%s" catchup="append" catchup-days="%s" catchup-source="?playseek={utc:YmdHMS}-{utcend:YmdHMS}" group-title="%s",%s\n' % (
                c["icon"], c["tvgId"], c["tvgName"], c["catchupDays"], group, c["tvgName"])
            #             line2 = homeLanAddress + '/udp/' + c["address"] + "\n"
            line2 = f'{c["catchupSource"]}\n'

            file.write(line)
            file.write(line2)
    file.close()
    print("Build m3u8 success.")

def generateUdpxyM3U8(file):
    file = open(file, "w", encoding='utf-8')
    name = '成都电信IPTV - ' + datetime.now(china_tz).strftime("%Y-%m-%d %H:%M:%S")
    # title = f'#EXTM3U name="{name}"' + ' x-tvg-url="https://epg.erw.cc/all.xml.gz" url-tvg="http://epg.51zmt.top:8000/e.xml.gz"\n'
    # title = f'#EXTM3U name="{name}"' + ' x-tvg-url="https://epg.erw.cc/all.xml.gz"\n'
    title = f'#EXTM3U name="{name}"' + ' x-tvg-url="https://epg.zsdc.eu.org/t.xml.gz"\n'
    file.write(title)
    for group in orders:
        v = [iptv for iptv in iptvList if iptv["group"] == group]
        for c in v:
            if "dup" in c:
                continue
            line = '#KODIPROP:inputstream=inputstream.ffmpegdirect\n#EXTINF:-1 tvg-logo="%s" tvg-id="%s" tvg-name="%s" catchup="default" catchup-days="%s" catchup-source="%s?playseek={utc:YmdHMS}-{utcend:YmdHMS}" group-title="%s",%s\n' % (
                c["icon"], c["tvgId"], c["tvgName"], c["catchupDays"], c["catchupSource"], group, c["tvgName"])
            line2 = homeLanAddress + '/udp/' + c["address"] + "\n"
            # line2 = f'{c["catchupSource"]}\n'

            file.write(line)
            file.write(line2)
    file.close()
    print("Build m3u8 success.")

def upload_convert_egp(m3u8_file, epg_m3u8_file):
    url = 'https://epg.51zmt.top:8001/api/upload/'
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Origin': 'https://epg.51zmt.top:8001',
        'Pragma': 'no-cache',
        'Referer': 'https://epg.51zmt.top:8001/',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }
    upload_file = open(m3u8_file, 'rb')
    files = {
        'myfile': ('iptv.m3u8', upload_file, 'audio/mpegurl')
    }

    response = requests.post(url, headers=headers, files=files, verify=False, timeout=(10, 60))
    print(response.text)
    upload_file.close()
    # 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    # 在HTML中查找下载链接
    download_link = soup.find('a', href=True)
    if download_link:
        file_url = download_link['href']
        # 获取绝对URL
        absolute_url = urljoin(urlparse(url).scheme + "://" + urlparse(url).hostname, file_url)
        # 下载文件
        file_response = requests.get(absolute_url, verify=False, timeout=(10, 60))
        # 将'your_file_name.extension'替换为所需的文件名和扩展名
        with open(epg_m3u8_file, 'w', encoding='utf-8') as file:
            file.write(file_response.content.decode())
            file.flush()
        print('文件成功下载！')
    else:
        print('在页面上找不到下载链接。')

def checkChannelExist(iptvList, channel):
    for item in iptvList:
        if item["tvgName"] == channel:
            print(f"频道 {channel} 已存在，跳过")
            return True
    return False

def generateHome():
    m3u8_file = './home/iptv.m3u8'
    # epg_m3u8_file = './home/iptv_epg.m3u8'
    generateM3U8(m3u8_file)
    print("生成m3u8完成")

    with open(m3u8_file, "r", encoding="utf-8") as f:
        content = f.read()
    content = content.replace("{utc:YmdHMS}-{utcend:YmdHMS}", "${(b)yyyyMMddHHmmss}-${(e)yyyyMMddHHmmss}")
    with open("./home/apt_iptv.m3u8", "w", encoding="utf-8") as f:
        f.write(content)
    print("生成APTV m3u8完成")

    udpxy_m3u8_file = './home/udpxy_iptv.m3u8'
    generateUdpxyM3U8(udpxy_m3u8_file)
    print("生成udpxy_m3u8完成")

    # upload_convert_egp(m3u8_file, epg_m3u8_file)
    # print("补齐egp文件完成")
    # fill_m3u8.fill_config(epg_m3u8_file, m3u8_file)
    # print("修正m3u8文件完成")
    # fill_erw_epg.fill_config(m3u8_file)
    # print("调整tvg-id支持erw的epg完成")


# exit(0)

# print("开始加载台标")
# mIcons = loadIcon()
# print("台标加载完成")
print("开始加载频道")
res = requests.get(sourceChengduMulticast, verify=False, timeout=(10, 60)).content
soup = BeautifulSoup(res, 'lxml')
# m = {}
iptvList = []

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
    group = filterCategory(name)
    # icon = findIcon(mIcons, name)
    icon = ''
    if os.path.exists(f'./logo/{name}.png'):
        icon = f'https://iptv.zsdc.eu.org/logo/{name}.png'

    # 判断name是否在m[group]中
    if not checkChannelExist(iptvList, name):
        iptvList.append({"id": td[0].string, "tvgId": name,"tvgName": name, "address": td[2].string, "catchupSource": td[6].string,
                         "catchupDays": td[3].string, "icon": icon, "group": group})
print("频道加载完成")

for item in iptvList: #支持4K频道EPG展示
    if item["tvgName"].find("4K") > 0 and checkChannelExist(iptvList, item["tvgName"].replace("4K", "")):
        item["tvgId"] = item["tvgName"].replace("4K", "")

generateHome()
