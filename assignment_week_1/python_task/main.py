import re
import urllib.request
import time
import math

def fetch_html(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        return resp.read().decode("utf-8", errors="ignore")

def extract_product_ids(html: str) -> list[str]:
    pattern = r'href="/prod/([A-Z0-9\-]+)"'
    ids = re.findall(pattern, html)
    return list(dict.fromkeys(ids))

def get_product_info(product_id):
    url = f"https://24h.pchome.com.tw/prod/{product_id}"
    html = fetch_html(url)

    # 1. 商品名稱
    name = ""
    name_match = re.search(r'"@type":"Product".*?"name":"(.*?)"', html, flags=re.DOTALL)
    if name_match:
        name = name_match.group(1).strip()

    # 2. 抓價格
    price = 0
    price_match = re.search(r'o-prodPrice__price[^>]*>\s*\$?([\d,]+)', html)
    if price_match:
        price_str = price_match.group(1).replace(",", "")
        try:
            price = int(price_str)
        except:
            price = 0

    # 3. 平均評分
    avg = 0.0
    score_match = re.search(r'c-indicator__number--ratingsTitle">([\d.]+)<', html)
    if score_match:
        try:
            avg = float(score_match.group(1))
        except:
            avg = 0.0

    # 4. 評論數
    total = 0
    count_match = re.search(r'共\s*(\d+)\s*則評價', html)
    if count_match:
        try:
            total = int(count_match.group(1))
        except:
            total = 0

    return name, price, avg, total

def get_all_product_ids() -> list[str]:
    all_ids = []
    page_num = 1

    while True:
        current_url = f"https://24h.pchome.com.tw/store/DSAA31?p={page_num}"
        html = fetch_html(current_url)
        ids = extract_product_ids(html)
        if len(ids) == 0:
            break

        all_ids.extend(ids)
        page_num += 1
        time.sleep(0.25)

    return all_ids

def get_product_info_map(product_ids: list[str]):
    product_map = {}

    for pid in product_ids:
        name, price, avg, total = get_product_info(pid)

        product_map[pid] = {
            "name": name,
            "price": price,
            "avg": avg,
            "total": total
        }

        #print(f"{pid} => name={name}, price={price}, avg={avg}, total={total}")
        time.sleep(0.25)

    return product_map

def main():
    #html = fetch_html('https://24h.pchome.com.tw/prod/DSAA31-A900IS8SK')
    #print(html)

    product_ids = get_all_product_ids()
    product_map = get_product_info_map(product_ids)

    #Task 1
    product_ids = get_all_product_ids()
    with open("products.txt", "w", encoding="utf-8") as f:
        for pid in product_ids:
            f.write(pid + "\n")

    #Task 2
    best_ids = [pid for pid, data in product_map.items() if data["total"] >= 1 and data["avg"] > 4.9]
    with open("best-products.txt", "w", encoding="utf-8") as f:
        for pid in best_ids:
            f.write(pid + "\n")

    #Task 3
    i5_prices = [data["price"] for data in product_map.values() if "i5" in data["name"].lower()]
    avg_price = sum(i5_prices) / len(i5_prices)
    print(avg_price)

    #Task 4
    prices = [data["price"] for data in product_map.values() if data["price"] > 0]
    N = len(prices)

    mean = sum(prices) / N
    variance = sum((p - mean) ** 2 for p in prices) / N  # 母體
    std = math.sqrt(variance)

    with open("standardization.csv", "w", encoding="utf-8") as f:
        f.write("ProductID,Price,PriceZScore\n")
        for pid, data in product_map.items():
            price = data["price"]
            if price > 0:
                z = (price - mean) / std if std != 0 else 0
                f.write(f"{pid},{price},{z}\n")
    
if __name__ == "__main__":
    main()