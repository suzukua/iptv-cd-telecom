#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re

tvg_id_pattern = re.compile(r'#EXTINF:-1.*?tvg-id="(?P<tvg_id>[^"]+)".*')
tvg_name_pattern = re.compile(r'#EXTINF:-1.*?tvg-name="(?P<tvg_name>[^"]+)".*')

tvg_id_replace_pattern = re.compile(r'(tvg-id=")([^"]*)(")')

def get_tvg_config_map(m3u8file_config):
    tvg_catchup_map = {}
    with open(m3u8file_config, 'rb') as f:
        lines = f.readlines()
        # 逐行处理
        for line in lines:
            line = line.decode('utf-8')
            id_match = tvg_id_pattern.match(line)
            name_match = tvg_name_pattern.match(line)
            if id_match and name_match:
                tvg_id = id_match.group('tvg_id')
                tvg_name = name_match.group('tvg_name')
                print(f"TVG Name: {tvg_name},tvg_id：{tvg_id}")
                print('-' * 40)
                tvg_catchup_map[tvg_name] = {"tvg_id": tvg_id}
    return tvg_catchup_map

# tvg_catchup_map = get_tvg_catchup_map("../home/iptv_org.m3u8")
# print(tvg_catchup_map)

def fill_config(m3u8file_config, m3u8file):
    # 从原文件中查找catchup-source
    tvg_catchup_map = get_tvg_config_map(m3u8file_config)
    with open(m3u8file, 'rb') as f:
        lines = f.readlines()
        # 逐行处理
        for index, line in enumerate(lines):
            line = line.decode('utf-8').strip()
            name_match = tvg_name_pattern.match(line)
            if name_match:
                tvg_name = name_match.group('tvg_name')
                if tvg_name in tvg_catchup_map:
                    tvg_id = tvg_catchup_map[tvg_name]['tvg_id']
                    fill_line = tvg_id_replace_pattern.sub(lambda m: f'{m.group(1)}{tvg_id}{m.group(3)}', line, )
                    print(fill_line)
                    lines[index] = fill_line
                else:
                    print(f"找不到对应的tvg配置：{tvg_name}")
        print(lines)

# fill_config('../home/iptv.m3u8', '../home/iptv_org.m3u8')