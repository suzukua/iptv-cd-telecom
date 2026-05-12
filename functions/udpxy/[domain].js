
export async function onRequest(context) {
    if (!context.params.domain){
        return new Response(`udpxy参数错误，例：https://iptv.zsdc.eu.org/udpxy/192.168.100.1:4022`);
    }
    const response = await fetch(`https://iptv.zsdc.eu.org/home/udpxy_iptv.m3u8`, {
        method: 'GET',
    });
    let m3uText = await response.text();
    let url = new URL(context.request.url)
    if (url.searchParams.get("aptv")) {
        m3uText = m3uText.replaceAll("{utc:YmdHMS}-{utcend:YmdHMS}", "${(b)yyyyMMddHHmmss}-${(e)yyyyMMddHHmmss}")
    }

    m3uText = m3uText.replaceAll("192.168.100.1:4022", context.params.domain)

    const fcc = url.searchParams.get("fcc")
    const r2hToken = url.searchParams.get("r2hToken")

    // 获取黑名单过滤参数
    const excludeParam = url.searchParams.get("exclude")

    let rtspProxy = url.searchParams.get("rtspProxy")
    if (rtspProxy && !rtspProxy.startsWith("http")) {
        rtspProxy = `http://${rtspProxy}`;
    }

    // 黑名单过滤频道
    if (excludeParam) {
        const keywords = excludeParam.split(',').map(k => k.trim())
        const out = []
        let pending = []  // 缓存 #KODIPROP 行，等 #EXTINF 确认是否保留
        let drop = false

        for (const line of m3uText.split("\n")) {
            if (line.startsWith("#KODIPROP")) {
                pending.push(line)
            } else if (line.startsWith("#EXTINF")) {
                const name = ((line.match(/tvg-name="([^"]*)"/) || [])[1] || "").toLowerCase()
                drop = keywords.some(k => name.includes(k.toLowerCase()))
                if (!drop) out.push(...pending, line)
                pending = []
            } else {
                if (!drop) out.push(line)
                if (!line.startsWith("#")) drop = false  // URL行之后重置
            }
        }

        m3uText = out.join("\n")
    }

    let lines = m3uText.split("\n")

    // 处理其他参数（fcc, rtspProxy等）
    lines.forEach(function(line,index){
        if (fcc && line.indexOf("/udp/") > 0) {
            let url = new URL(line)
            line = (line += `${url.searchParams.size > 0 ? '&' : '?'}fcc=${fcc}`);
            if (r2hToken) {
                url = new URL(line)
                line = (line += `${url.searchParams.size > 0 ? '&' : '?'}r2h-token=${r2hToken}`);
            }
        }
        if (rtspProxy && line.indexOf("catchup-source=\"rtsp://") > 0) {
            line = line.replaceAll("catchup-source=\"rtsp://", `catchup-source="${rtspProxy}/rtsp/`);
            if (r2hToken) {
                const match = line.match(/catchup-source="([^"]+)"/);
                if (match) {
                    let url = new URL(match[1]);
                    let tmp = `${match[1]}${url.searchParams.size > 0 ? '&' : '?'}r2h-token=${r2hToken}`;
                    line = line.replaceAll(match[1], tmp);
                }
            }
        }
        lines[index] = line;
    })
    m3uText = lines.join("\n")

    return new Response(m3uText);
}