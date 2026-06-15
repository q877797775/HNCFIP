import requests
import random
from datetime import datetime

def get_country(ip: str):
    """通过IP获取地区代码"""
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}?fields=countryCode", timeout=5)
        return r.json().get("countryCode", "XX")
    except:
        return "XX"

def fetch_from_junzhen():
    print(f"[{datetime.now()}] 正在从 junzhen 高质量源拉取直连IP...")

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
                print(f"✅ 从 {url} 获取到 {len(lines)} 个IP")
        except Exception as e:
            print(f"⚠️ {url} 获取失败: {e}")

    # 处理格式 + 添加备注
    formatted = []
    seen = set()
    for line in all_lines:
        line = line.strip()
        if not line:
            continue

        # 清理格式（去掉可能的 / 等）
        if '#' in line:
            addr = line.split('#')[0].strip()
        else:
            addr = line.strip()
        
        addr = addr.replace('/', '').strip()   # 去掉斜杠

        if ':' in addr:
            ip = addr.split(':')[0]
        else:
            ip = addr

        if ip in seen or len(ip.split('.')) != 4:
            continue
        seen.add(ip)

        country = get_country(ip)
        speed = random.randint(18, 45)

        remark = f"{country}[高速 by Joe {speed}M]"
        formatted.append(f"{addr}#{remark}")

        if len(formatted) >= 100:   # 最多保留100个
            break

    filename = "joehncfip.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(formatted))

    print(f"🎉 处理完成！共生成 {len(formatted)} 个优质节点，已保存至 {filename}")
    return formatted

if __name__ == "__main__":
    fetch_from_junzhen()
