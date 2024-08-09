#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pytz
import requests, re
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from datetime import datetime

tvg_name_pattern = re.compile(r'#EXTINF:-1.*?tvg-name="(?P<tvg_name>[^"]+)".*')

tvg_id_replace_pattern = re.compile(r'(tvg-id=")([^"]*)(")')

name_mapping = {"CCTV5+": "CCTV5plus", "旅游卫视": "海南卫视","卡酷动画":"卡酷少儿",
                "中国教育1台": "CETV1", "中国教育2台": "CETV2","中国教育3台": "CETV3",
                "中国教育4台": "CETV4", "SCTV2": "四川文化旅游", "SCTV3": "四川经济",
                "SCTV4": "四川新闻", "SCTV5": "四川影视文艺", "SCTV7": "四川妇女儿童",
                "SCTV8": "四川科教", "CDTV1": "成都新闻综合", "CDTV2": "成都经济资讯",
                "CDTV3": "成都都市生活", "CDTV4": "成都影视文艺", "CDTV5": "成都公共", "CDTV6": "成都少儿"}


file_name = './home/epg.erw.cc.html'
def download_channel_list():
    channel = []
    try:
        res = requests.get("https://epg.erw.cc/", timeout=(10, 30))
        # Open a local file with write-binary mode
        with open(file_name, 'wb') as f:
            # Write the content of the response to the file
            f.write(res.content)
    except BaseException as err:
        print(f'HTTP error occurred: {err}')

    with open(file_name, 'r', encoding='utf-8') as file:
        content = file.read()
    soup = BeautifulSoup(content, 'lxml')
    for tr in soup.find_all(name='tr', class_='channel-row'):
        tds = tr.find_all(name='td')
        if len(tds) < 5:
            continue
        channel.append({"tvg_name": tds[1].string, "tvg_id": tds[2].string})
    print(f'共抓取到{len(channel)}个频道')
    return channel


def get_tvg_config(channel_config_list, tvg_name):
    for config in channel_config_list:
        if config['tvg_name'] == tvg_name:
            return config
        if tvg_name in name_mapping:
            if config['tvg_name'] == name_mapping[tvg_name]:
                return config
        if len(config['tvg_name']) > 2 and config['tvg_name'].endswith("频道") and config['tvg_name'][:-2] == tvg_name:
            return config

def fill_config(m3u8file):
    channel_config_list = download_channel_list()
    with open(m3u8file, 'r+', encoding='utf-8') as f:
        lines = f.readlines()
        f.seek(0)  # 将文件指针移动到文件开头
        # 逐行处理
        for index, line in enumerate(lines):
            name_match = tvg_name_pattern.match(line)
            if name_match:
                tvg_name = name_match.group('tvg_name')
                tvg_config = get_tvg_config(channel_config_list, tvg_name)
                if tvg_config:
                    tvg_id = tvg_config['tvg_id']
                    if tvg_id and tvg_id != "":
                        line = tvg_id_replace_pattern.sub(lambda m: f'{m.group(1)}{tvg_id}{m.group(3)}', line)
                else:
                    print(f"erw.epg  找不到对应的tvg配置：{tvg_name}")
            f.write(line)