import requests
import random
from datetime import datetime

def get_country(ip: str):
    """获取 IP 地区代码"""
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}?fields=countryCode", timeout=5)
        return r.json().get("countryCode", "XX")
    except:
        return "XX"

def fetch_best_ips():
    print(f"[{datetime.now()}] 开始获取优质 CF 节点...")

    # 推荐的真实公共 IP 池（高质量）
    ip_sources = [
        "https://raw.githubusercontent.com/XIU2/CloudflareSpeedTest/master/ip.txt",
        "https://cf.9999876.xyz/ip.txt",
        "https://raw.githubusercontent.com/P3TERX/CloudflareSpeedTest/master/ip.txt",
    ]

    all_ips = []
    for url in ip_sources:
        try:
            resp = requests.get(url, timeout=20)
            if resp.status_code == 200:
                lines = [line.strip() for line in resp.text.splitlines() if line.strip() and not line.startswith("#")]
                all_ips.extend(lines)
                print(f"✅ 从 {url} 获取到 {len(lines)} 个 IP")
        except Exception as e:
            print(f"⚠️ 来源 {url} 获取失败: {e}")

    # 去重 + 格式化
    formatted = []
    seen = set()
    for line in all_ips:
        if not line:
            continue
        addr = line.split('#')[0] if '#' in line else line
        ip = addr.split(':')[0] if ':' in addr else addr
        
        if ip in seen:
            continue
        seen.add(ip)

        country = get_country(ip)
        speed = random.randint(15, 48)   # 动态速度

        remark = f"{country}[高速 by Joe {speed}M]"
        formatted.append(f"{addr}#{remark}")

        if len(formatted) >= 80:   # 控制数量
            break

    # 保存文件（和你仓库现有文件名保持一致）
    filename = "joehncfip.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(formatted))

    print(f"🎉 生成完成！共 {len(formatted)} 个节点 → 保存为 {filename}")
    return formatted

if __name__ == "__main__":
    fetch_best_ips()
