
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
    if (fcc) {
        let lines = m3uText.split("\n")
        lines.forEach(function(line,index){
            if (line.indexOf("/udp/") > 0) {
                let url = new URL(line)
                if (url.searchParams.size > 0){
                    line += `&fcc=${fcc}`
                } else {
                    line += `?fcc=${fcc}`
                }
                lines[index] = line;
            }
        })
        m3uText = lines.join("\n")
    }

    return new Response(m3uText);
}