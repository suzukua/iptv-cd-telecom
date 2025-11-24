## CD Telecom IPTV直播源，成都电信IPTV直播源，四川电信IPTV直播源，机顶盒替代方案

### 支持tvbox、KODI、fileball、APTV、mytv-android等。支持回看、时移（每周不定时更新）

![badge](https://github.com/suzukua/iptv-cd-telecom/actions/workflows/cloudflare-pages.yml/badge.svg)

#### 更新时间：2025-11-25 07:11:16 共 152 条频道信息

#### 组播转单播地址(兼容udpxy、msd_lite、rtp2httpd)，[FCC服务器地址](https://github.com/stackia/rtp2httpd/blob/main/cn-fcc-collection.md)
```markdown
# 自定义单播地址：https://iptv.zsdc.eu.org/udpxy/[ip:port]
示例1：https://iptv.zsdc.eu.org/udpxy/192.168.100.2:4022
示例2(APTV时区兼容版)：https://iptv.zsdc.eu.org/udpxy/192.168.100.2:4022?aptv=1&fcc=182.139.234.40:8027

目前支持参数说明：
aptv=1, rtsp回看时间参数(playseek=${(b)yyyyMMddHHmmss}-${(e)yyyyMMddHHmmss}), 支持APTV、mytv-android等
fcc=182.139.234.40:8027, 支持rtp2httpd FCC快速换台模式
```

#### 电信官方单播源，支持时移（已解决部分4K频道无法观看的问题：使用组播转单播）
```markdown
# 官方单播源
https://iptv.zsdc.eu.org/home/iptv.m3u8

# APTV时区兼容版
https://iptv.zsdc.eu.org/home/apt_iptv.m3u8
```

----

配套EPG电子节目单数据(每天多次更新)，支持央视、卫视超100套频道

[EPG节目单](https://epg.zsdc.eu.org)
        
    https://epg.zsdc.eu.org

[华硕路由单线复用、IPTV融合](https://github.com/suzukua/asus-router-shell)

    https://github.com/suzukua/asus-router-shell

###### 有问题？更新不及时？[联系我](https://github.com/suzukua/iptv-cd-telecom/issues)
