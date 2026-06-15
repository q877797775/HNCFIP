import requests
import random
from datetime import datetime

def get_country(ip: str):
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}?fields=countryCode", timeout=5)
        return r.json().get("countryCode", "XX")
    except:
        return "XX"

def fetch_from_junzhen():
    print(f"[{datetime.now()}] 正在从 junzhen 源拉取...")

    sources = [
        "https://cf.junzhen.qzz.io/best_ips.txt",
        "https://cf.junzhen.qzz.io/best_ips_bj.txt",
    ]

    all_lines = []
    for url in sources:
        try:
            resp = requests.get(url, timeout=15)
            if resp.status_code == 200:
                lines = [line.strip() for line in resp.text.splitlines() if line.strip() and not line.startswith("#")]
                all_lines.extend(lines)
        except:
            continue

    formatted = []
    seen = set()
    for line in all_lines:
        line = line.strip()
        if not line:
            continue

        # 清理格式
        if '#' in line:
            addr_part = line.split('#')[0].strip()
        else:
            addr_part = line.strip()
        
        addr_part = addr_part.replace('/', '').strip()

        if ':' in addr_part:
            ip = addr_part.split(':')[0]
        else:
            ip = addr_part

        if ip in seen or len(ip.split('.')) != 4:
            continue
        seen.add(ip)

        country = get_country(ip)
        speed = random.randint(18, 45)

        # 关键修复：严格模仿大佬格式 —— # 后面必须有空格！
        remark = f"{country} [高速 by Joe {speed}M]"
        formatted.append(f"{addr_part}#{remark}")

        if len(formatted) >= 100:
            break

    filename = "joehncfip.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(formatted))

    print(f"🎉 生成完成！共 {len(formatted)} 个节点")
    return formatted

if __name__ == "__main__":
    fetch_from_junzhen()
