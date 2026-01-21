# 成都/四川电信 IPTV 直播源

![badge](https://github.com/suzukua/iptv-cd-telecom/actions/workflows/cloudflare-pages.yml/badge.svg)

> 📺 IPTV机顶盒替代方案 | 支持回看、时移 | 每周不定时更新  
> 📅 更新时间：2026-01-22 07:11:14 | 共 150 条频道信息

## ✨ 特性

- 🎬 **播放器支持**：tvbox、KODI、fileball、APTV、mytv-android 等
- 🔄 **回看时移**：支持节目回看和时移功能
- 📡 **多种方式**：官方单播源、组播转单播（udpxy/msd_lite/rtp2httpd）
- 🎯 **4K 支持**：已解决部分 4K 频道播放问题
- 📺 **EPG 节目单**：每天多次更新，覆盖央视、卫视超 100 套频道

## 📖 使用说明

### 方式一：官方单播源（推荐新手）

直接使用以下地址即可播放，支持时移功能：

```
官方单播源：
https://iptv.zsdc.eu.org/home/iptv.m3u8

APTV 时区兼容版：
https://iptv.zsdc.eu.org/home/apt_iptv.m3u8
```

### 方式二：组播转单播（高级用户）

兼容 udpxy、msd_lite、rtp2httpd 等工具。

**地址格式：**
```
https://iptv.zsdc.eu.org/udpxy/[ip:port]
```

**使用示例：**

```
# 示例 1：基础用法
https://iptv.zsdc.eu.org/udpxy/192.168.100.2:4022

# 示例 2：APTV 时区兼容 + FCC 快速换台 + RTSP 代理
https://iptv.zsdc.eu.org/udpxy/192.168.100.2:4022?aptv=1&fcc=182.139.234.40:8027&rtspProxy=192.168.100.2:4022

# 示例 3：回放转单播（RTSP 转 HTTP）
https://iptv.zsdc.eu.org/udpxy/192.168.100.2:4022?fcc=182.139.234.40:8027&rtspProxy=192.168.100.2:4022
```

**参数说明：**

| 参数 | 说明 | 示例 |
|------|------|------|
| `aptv=1` | 启用 APTV 时区兼容，回看时间参数格式：`playseek=${(b)yyyyMMddHHmmss}-${(e)yyyyMMddHHmmss}` | 支持 APTV、mytv-android 等 |
| `fcc=host:port` | 启用 rtp2httpd FCC 快速换台模式，[FCC 服务器地址列表](https://github.com/stackia/rtp2httpd/blob/main/docs/cn-fcc-collection.md) | `fcc=182.139.234.40:8027` |
| `rtspProxy=host:port` | RTSP 转 HTTP 播放（rtp2httpd），默认 http 协议，可指定 https | `rtspProxy=192.168.100.2:4022` 或 `rtspProxy=https://192.168.100.2:4022` |

## 📺 EPG 电子节目单

每天多次更新，支持央视、卫视超 100 套频道：

```
https://epg.zsdc.eu.org
```

## 🔧 相关资源

### 华硕路由单线复用 / IPTV 融合

如果你使用华硕路由器，可以参考以下项目实现单线复用和 IPTV 融合：

- 项目地址：[asus-router-shell](https://github.com/suzukua/asus-router-shell)
- 双网融合后无法观看回放？参考 [IPTV 路由配置脚本](https://github.com/suzukua/asus-router-shell/blob/main/scripts/iptv.script#L31-L32)

## 💬 问题反馈

如有问题或更新不及时，欢迎提交 [Issue](https://github.com/suzukua/iptv-cd-telecom/issues)

## 📝 声明

本项目仅供学习交流使用，请在合法合规的范围内使用本项目提供的服务。
