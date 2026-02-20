# 🎬 成都/四川电信 IPTV 直播源

![badge](https://github.com/suzukua/iptv-cd-telecom/actions/workflows/cloudflare-pages.yml/badge.svg)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

> 📺 **IPTV 机顶盒替代方案** | 支持回看、时移 | 每周不定时更新  
> 📅 **更新时间**：2026-02-21 07:11:13 | 共 **150** 条频道信息

---

## ✨ 核心特性

- 🎬 **广泛兼容**：支持 tvbox、KODI、fileball、APTV、mytv-android 等主流播放器
- 🔄 **回看时移**：支持节目回看和时移功能，不错过精彩内容
- 📡 **灵活接入**：提供官方单播源、组播转单播（udpxy/msd_lite/rtp2httpd）多种方式
- 🎯 **4K 超清**：已解决部分 4K 频道播放问题，享受超高清画质
- 📺 **完整节目单**：每天多次更新 EPG，覆盖央视、卫视超 100 套频道

---

## 📖 使用指南

### 🚀 方式一：官方单播源（推荐新手）

直接复制以下地址到播放器即可使用，无需额外配置：

**标准版（推荐）：**
```
https://iptv.zsdc.eu.org/home/iptv.m3u8
```

**APTV 兼容版：**
```
https://iptv.zsdc.eu.org/home/apt_iptv.m3u8
```

> 💡 **提示**：两个版本都支持时移功能，APTV 版针对时区兼容性进行了优化

---

### 🔧 方式二：组播转单播（高级用户）

适用于已搭建 udpxy、msd_lite、rtp2httpd 等工具的用户。

#### 📌 地址格式

```
https://iptv.zsdc.eu.org/udpxy/[ip:port]?[参数]
```

#### 🎯 使用示例

**示例 1 - 基础用法：**
```
https://iptv.zsdc.eu.org/udpxy/192.168.100.2:4022
```

**示例 2 - APTV + FCC + RTSP 代理：**
```
https://iptv.zsdc.eu.org/udpxy/192.168.100.2:4022?aptv=1&fcc=182.139.234.40:8027&rtspProxy=192.168.100.2:4022
```

**示例 3 - 回放转单播（RTSP → HTTP）：**
```
https://iptv.zsdc.eu.org/udpxy/192.168.100.2:4022?fcc=182.139.234.40:8027&rtspProxy=192.168.100.2:4022
```

#### 📋 参数说明

| 参数 | 功能描述 | 使用示例 | 适用场景                   |
|------|---------|---------|------------------------|
| `aptv=1` | 启用 APTV 时区兼容 | `aptv=1` | APTV、mytv-android 等播放器 |
| `fcc=host:port` | 启用 FCC 快速换台模式 | `fcc=182.139.234.40:8027` | 需要快速切换频道的场景            |
| `rtspProxy=host:port` | RTSP 转 HTTP 播放 | `rtspProxy=192.168.100.2:4022` | 不支持 RTSP 协议的播放器/外网回看   |

> 📝 **说明**：
> - 回看时间参数格式：`playseek=${(b)yyyyMMddHHmmss}-${(e)yyyyMMddHHmmss}`
> - FCC 服务器地址列表：[查看更多](https://github.com/stackia/rtp2httpd/blob/main/docs/cn-fcc-collection.md)
> - `rtspProxy` 支持 HTTP/HTTPS 协议，可指定 `rtspProxy=https://192.168.100.2:4022`

---

## 📺 EPG 电子节目单

每天自动更新多次，覆盖 **央视、卫视超 100 套频道**：

```
https://epg.zsdc.eu.org/t.xml.gz
```

> 🔄 **更新频率**：每天多次自动更新，确保节目单准确性

---

## 🔧 相关资源

### 📡 华硕路由器单线复用 / IPTV 融合

如果你使用华硕路由器，可参考以下项目实现单线复用和 IPTV 融合：

- 🔗 **项目地址**：[asus-router-shell](https://github.com/suzukua/asus-router-shell)
- ⚙️ **IPTV 配置脚本**：[查看配置](https://github.com/suzukua/asus-router-shell/blob/main/scripts/iptv.script#L31-L32)

> ⚠️ **注意**：双网融合后无法观看回放？请参考上述配置脚本进行调整

---

## 💬 问题反馈

遇到问题或有建议？欢迎通过以下方式反馈：

- 📮 **提交 Issue**：[GitHub Issues](https://github.com/suzukua/iptv-cd-telecom/issues)
- 💡 **功能建议**：欢迎在 Issues 中提出你的想法

> 🙏 **提示**：提交问题时请详细描述你的使用场景和遇到的错误信息

---

## 📝 免责声明

- ⚖️ 本项目仅供 **学习交流** 使用
- 🔒 请在 **合法合规** 的范围内使用本项目提供的服务
- 📌 本项目不提供任何视频内容，所有内容来源于公开的 IPTV 服务

---