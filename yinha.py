import asyncio
import aiohttp
import pandas as pd
import time
import ssl

# ================= 設定參數 =================
BASE_URL = "https://wpapi.ldjzmr.top/admin/platform_transfer"
TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczovL3dwYXBpLmxkanptci50b3AvYWRtaW4vbG9naW4iLCJpYXQiOjE3NzAyMjU1OTIsImV4cCI6MTgwMTc2MTU5MiwibmJmIjoxNzcwMjI1NTkyLCJqdGkiOiJiQmZUbkhYeUU2VUZKWWgzIiwic3ViIjoiNDcwIiwicHJ2IjoiNzIzNDlhZmZkYTA0NGRjMmFkNzBhMzllZjE1MTYzZWE2N2E3MzMxMyJ9.Hsgr2kkguL77IFnH3AqL9Oz8QZx24efuiUiKKQVlm4c"
PAGE_SIZE = 100 
OUTPUT_FILE = "品牌積分資料_完整導出.xlsx"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*"
}

# ================= 核心邏輯 =================

def extract_list(res_json):
    """自動偵測 API 回傳的資料清單位置"""
    data_obj = res_json.get('data', {})
    # 1. 如果 data 直接是 list
    if isinstance(data_obj, list):
        return data_obj
    # 2. 嘗試常見的清單欄位名稱
    for key in ['list', 'data', 'rows', 'items']:
        if isinstance(data_obj.get(key), list):
            return data_obj[key]
    return []

async def fetch_page(session, page, semaphore):
    async with semaphore:
        url = f"{BASE_URL}?pagenum={page}&pagesize={PAGE_SIZE}"
        try:
            async with session.get(url, headers=headers, timeout=15) as response:
                if response.status == 200:
                    res_json = await response.json()
                    return extract_list(res_json)
                else:
                    print(f"❌ 第 {page} 頁請求失敗: {response.status}")
                    return []
        except Exception as e:
            print(f"🧨 第 {page} 頁連線錯誤: {e}")
            return []

async def main():
    start_time = time.time()
    
    # 解決你截圖中的 SSL 驗證錯誤
    connector = aiohttp.TCPConnector(ssl=False)
    semaphore = asyncio.Semaphore(10) # 限制同時連線數，保護伺服器

    async with aiohttp.ClientSession(connector=connector) as session:
        # 1. 取得總頁數
        print("🔍 正在檢查資料總量...")
        async with session.get(f"{BASE_URL}?pagenum=1&pagesize={PAGE_SIZE}", headers=headers) as resp:
            if resp.status != 200:
                print(f"❌ 無法連線 API (Status: {resp.status})，請確認 Token。")
                return
            init_data = await resp.json()
            total_count = init_data.get('data', {}).get('total', 0)
            
        if total_count == 0:
            print("📭 找不到任何數據。")
            return

        total_pages = (total_count // PAGE_SIZE) + (1 if total_count % PAGE_SIZE > 0 else 0)
        print(f"📊 總筆數: {total_count}，預計抓取 {total_pages} 頁...")

        # 2. 並行抓取
        tasks = [fetch_page(session, page, semaphore) for page in range(1, total_pages + 1)]
        pages_results = await asyncio.gather(*tasks)

        # 3. 合併數據
        all_data = [item for sublist in pages_results for item in sublist]
        print(f"✅ 抓取完成，共取得 {len(all_data)} 筆資料。")

        # 4. 轉換 Excel
        if all_data:
            df = pd.DataFrame(all_data)
            
            # 對照截圖中的中文標題
            mapping = {
                "id": "ID",
                "order_no": "流水號",
                "username": "用戶名稱",
                "mobile": "用戶手機號",
                "machine_name": "機器名稱",
                "machine_no": "機器編號",
                "platform": "平台",
                "type_name": "交易類型",
                "amount": "轉入轉出數量",
                "points": "積分數量",
                "created_at": "創建時間"
            }
            df.rename(columns={k: v for k, v in mapping.items() if k in df.columns}, inplace=True)

            print(f"💾 正在儲存至 {OUTPUT_FILE}...")
            df.to_excel(OUTPUT_FILE, index=False)
            print(f"🎉 任務成功！耗時: {time.time() - start_time:.2f} 秒")
        else:
            print("❌ 錯誤：雖然有總筆數，但未抓到任何詳細資料列。")

if __name__ == "__main__":
    asyncio.run(main())