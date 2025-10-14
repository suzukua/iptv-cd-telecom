
export async function onRequest(context) {
    if (!context.params.udpxy){
        return new Response(`udpxy参数错误，例：https://iptv.zsdc.eu.org/udpxy/192.168.100.1:4022`);
    }
    const response = await fetch(`https://iptv.zsdc.eu.org/home/udpxy_iptv.m3u8`, {
        method: 'GET',
    });
    let m3uText = await response.text();
    m3uText = m3uText.replaceAll("192.168.100.1:4022", context.params.udpxy)
    let url = new URL(context.request.url)
    if (url.searchParams.get("aptv")) {
        m3uText = m3uText.replaceAll("{utc:YmdHMS}-{utcend:YmdHMS}", "${(b)yyyyMMddHHmmss}-${(e)yyyyMMddHHmmss}")
    }
    return new Response(m3uText);
}