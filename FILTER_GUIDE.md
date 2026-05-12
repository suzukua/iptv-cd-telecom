# 📋 频道过滤功能使用指南

## 功能说明

频道过滤功能允许你通过URL参数自定义显示的频道列表，支持包含和排除两种过滤模式。

## 参数说明

### include 参数
- **功能**：只保留包含指定关键字的频道
- **语法**：`include=关键字1,关键字2,关键字3`
- **示例**：`include=CCTV` - 只显示CCTV频道

### exclude 参数
- **功能**：排除包含指定关键字的频道
- **语法**：`exclude=关键字1,关键字2,关键字3`
- **示例**：`exclude=4K,专区` - 排除所有4K和专区频道

## 使用示例

### 1️⃣ 只显示央视频道
```
https://iptv.zsdc.eu.org/udpxy/192.168.100.2:4022?include=CCTV
```
结果：只显示CCTV1、CCTV2、CCTV3等央视频道

### 2️⃣ 只显示卫视频道
```
https://iptv.zsdc.eu.org/udpxy/192.168.100.2:4022?include=卫视
```
结果：只显示湖南卫视、浙江卫视、江苏卫视等卫视频道

### 3️⃣ 排除4K频道
```
https://iptv.zsdc.eu.org/udpxy/192.168.100.2:4022?exclude=4K
```
结果：显示所有非4K频道

### 4️⃣ 排除专区频道
```
https://iptv.zsdc.eu.org/udpxy/192.168.100.2:4022?exclude=专区
```
结果：排除所有专区频道（如电影专区、少儿专区等）

### 5️⃣ 只显示央视和卫视
```
https://iptv.zsdc.eu.org/udpxy/192.168.100.2:4022?include=CCTV,卫视
```
结果：显示所有央视和卫视频道

### 6️⃣ 显示卫视但排除4K版本
```
https://iptv.zsdc.eu.org/udpxy/192.168.100.2:4022?include=卫视&exclude=4K
```
结果：只显示卫视频道，但不包括4K版本

### 7️⃣ 显示四川本地频道
```
https://iptv.zsdc.eu.org/udpxy/192.168.100.2:4022?include=SCTV,CDTV,四川
```
结果：显示所有四川本地频道

### 8️⃣ 组合其他参数使用
```
https://iptv.zsdc.eu.org/udpxy/192.168.100.2:4022?include=卫视&exclude=4K&aptv=1&fcc=182.139.234.40:8027
```
结果：显示非4K的卫视频道，并启用APTV兼容和FCC快速换台

## 注意事项

⚠️ **重要提示**：

1. **关键字区分大小写**
   - `CCTV` 和 `cctv` 是不同的关键字
   - 建议使用频道列表中的原始名称

2. **多个关键字使用英文逗号分隔**
   - ✅ 正确：`include=CCTV,卫视`
   - ❌ 错误：`include=CCTV，卫视`（使用了中文逗号）

3. **关键字匹配规则**
   - 匹配频道名称中的任意位置
   - 例如：`CCTV` 会匹配 `CCTV1`、`CCTV2`、`CCTV4K` 等
   - `4K` 会匹配 `CCTV4K`、`湖南卫视4K` 等

4. **include 和 exclude 同时使用**
   - 先应用 `include` 规则筛选频道
   - 再应用 `exclude` 规则排除频道
   - 示例：`include=卫视&exclude=4K` 表示"显示所有卫视，但排除4K版本"

## 常见应用场景

### 场景1：老年人用户 - 只看央视和地方台
```
?include=CCTV,SCTV,CDTV
```

### 场景2：追剧用户 - 只看主流卫视
```
?include=湖南,浙江,江苏,东方,北京&exclude=4K
```

### 场景3：儿童模式 - 只看少儿频道
```
?include=少儿,动画,卡通
```

### 场景4：电影爱好者 - 只看电影频道
```
?include=电影,影院,CHC
```

### 场景5：精简列表 - 排除所有专区和4K
```
?exclude=专区,4K
```

## 技术原理

过滤功能基于 `tvg-name` 属性进行匹配：
```m3u
#EXTINF:-1 tvg-name="CCTV1" ...
```

当你使用 `include=CCTV` 时，系统会检查 `tvg-name` 中是否包含 "CCTV" 字符串。

## 反馈与建议

如果你在使用过滤功能时遇到问题，或有改进建议，欢迎：
- 提交 Issue：https://github.com/suzukua/iptv-cd-telecom/issues
- 分享你的使用场景和配置

---

💡 **提示**：建议将常用的过滤URL保存为书签，方便快速访问！

