import requests
import time

url = "https://wpadmin.ldjzmr.top/"
interval = 1  # 每秒固定一次

while True:
    start = time.time()

    try:
        r = requests.get(url, timeout=5)
        latency = (time.time() - start) * 1000
        print(f"{time.strftime('%H:%M:%S')} | {r.status_code} | {latency:.2f} ms")
    except Exception as e:
        print("Failed:", e)

    elapsed = time.time() - start
    time.sleep(max(0, interval - elapsed))
