#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re

tvg_id_pattern = re.compile(r'#EXTINF:-1.*?tvg-id="(?P<tvg_id>[^"]+)".*')
tvg_name_pattern = re.compile(r'#EXTINF:-1.*?tvg-name="(?P<tvg_name>[^"]+)".*')

tvg_id_replace_pattern = re.compile(r'(tvg-id=")([^"]*)(")')
tvg_name_replace_pattern = re.compile(r'(tvg-name=")([^"]*)(")')

def fullwidth_to_halfwidth(ustring):
    """将字符串中的全角字符转换为半角字符"""
    result = []
    for uchar in ustring:
        inside_code = ord(uchar)
        if inside_code == 0x3000:  # 全角空格
            inside_code = 0x0020
        elif 0xFF01 <= inside_code <= 0xFF5E:  # 全角字符（除空格）
            inside_code -= 0xFEE0
        result.append(chr(inside_code))
    return ''.join(result)

def get_tvg_config(m3u8file_config, tvg_name):
    with open(m3u8file_config, 'rb') as f:
        lines = f.readlines()
        # 逐行处理
        for line in lines:
            line = line.decode('utf-8')
            half_tvg_name = fullwidth_to_halfwidth(tvg_name)
            name_include_match = re.compile(fr'#EXTINF:-1.*?({re.escape(tvg_name)}|{re.escape(half_tvg_name)})', re.IGNORECASE).match(line)
            if name_include_match:
                id_match = tvg_id_pattern.match(line)
                name_match = tvg_name_pattern.match(line)
                if id_match and name_match:
                    tvg_id = id_match.group('tvg_id')
                    tvg_new_name = name_match.group('tvg_name')
                    print(f"TVG Name: {tvg_name}, TVG new Name: {tvg_new_name}, tvg_id：{tvg_id}")
                    print('-' * 40)
                    return {"tvg_name": tvg_new_name, "tvg_id": tvg_id}

def fill_config(m3u8file_config, m3u8file):
    # 从原文件中查找catchup-source
    # tvg_catchup_map = get_tvg_config_map(m3u8file_config)
    with open(m3u8file, 'r+', encoding='utf-8') as f:
        lines = f.readlines()
        f.seek(0)  # 将文件指针移动到文件开头
        # 逐行处理
        for index, line in enumerate(lines):
            name_match = tvg_name_pattern.match(line)
            if name_match:
                tvg_name = name_match.group('tvg_name')
                tvg_config = get_tvg_config(m3u8file_config, tvg_name)
                if tvg_config:
                    tvg_id = tvg_config['tvg_id']
                    tvg_new_name = tvg_config['tvg_name']
                    line = tvg_id_replace_pattern.sub(lambda m: f'{m.group(1)}{tvg_id}{m.group(3)}', line)
                    # line = tvg_name_replace_pattern.sub(lambda m: f'{m.group(1)}{tvg_new_name}{m.group(3)}', line)
                else:
                    print(f"找不到对应的tvg配置：{tvg_name}")
            f.write(line)

# fill_config('../home/iptv_epg.m3u8', '../home/iptv.m3u8')

# get_tvg_config('../home/iptv_epg.m3u8', 'CCTV5＋')