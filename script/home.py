#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import m3u8
import sys
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import strict_rfc3339
import re


#with open('./sctvmulticast.html') as f:
#   res=f.read()

sourceTvboxIptv="https://raw.githubusercontent.com/gaotianliuyun/gao/master/list.txt"
sourceIcon51ZMT="http://epg.51zmt.top:8000"
sourceChengduMulticast="http://epg.51zmt.top:8000/sctvmulticast.html"
homeLanAddress="http://192.168.100.1:8686"

groupCCTV=["CCTV", "CETV", "CGTN"]
groupWS=[ "卫视"]
groupSC=["SCTV", "四川", "CDTV", "熊猫", "峨眉", "成都"]
listUnused=["单音轨", "画中画", "热门", "直播室", "爱", "92"]


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

def appendOnlineIptvFromTvbox(listIptv):
    onlineIptv = requests.get(sourceTvboxIptv).content
    lines = onlineIptv.splitlines()

    for line in lines:
        line=line.decode('utf-8')
        groupMatch = re.search(r'(.+),#genre#', line)
        if groupMatch:
            g = groupMatch.group(1)
            if g not in listIptv:
                listIptv[g] = []
            continue
        if g == "YouTube":
            continue

        v=line.split(',')

        if checkChannelExist(listIptv, v[0]):
            listIptv[g].append({"id": getID(), "name": v[0], "address": v[1], "dup": True})
            continue
        else:
            listIptv[g].append({"id": getID(), "name": v[0], "address": v[1]})


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
    title = '#EXTM3U name=\"' + name + '\"' + ' url-tvg=\"http://epg.51zmt.top:8000/e.xml,https://epg.112114.xyz/pp.xml\"\n\n'
    file.write(title)

    for k, v in m.items():
        for c in v:
            if "dup" in c:
                continue

            if "ct" in c:
                line = '#EXTINF:-1 tvg-logo="%s" tvg-id="%s" tvg-name="%s" group-title="%s",%s\n' % (c["icon"], c["id"], c["name"], k, c["name"])
                line2 = homeLanAddress + '/rtp/' + c["address"] + "\n"
            else:
                line = '#EXTINF:-1 tvg-id="%s" tvg-name="%s" group-title="%s",%s\n' % (getID(), c["name"], k, c["name"])
                line2 = c["address"] + "\n"

            file.write(line)
            file.write(line2)

    file.close()
    print("Build m3u8 success.")

def generateTXT(file):
    file=open(file, "w")
    for k, v in m.items():
        line = '%s,#genre#\n' % (k)
        file.write(line)

        for c in v:
            line = '%s,%s/rtp/%s\n' % (c["name"], homeLanAddress, c["address"])
            if "ct" not in c:
                line = '%s,%s\n' % (c["name"], c["address"])

            file.write(line)

    file.close()
    print("Build txt success.")


def generateHome():
    generateM3U8("./home/iptv.m3u8")
    generateTXT("./home/iptv.txt")

#exit(0)


mIcons = loadIcon()

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

    m[group].append({"id": td[0].string, "name": name, "address": td[2].string, "ct": True, "icon": icon})


appendOnlineIptvFromTvbox(m)

generateHome()




#res = requests.get("https://raw.githubusercontent.com/iptv-org/iptv/master/streams/hk.m3u")

