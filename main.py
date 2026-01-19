import requests
import pandas as pd

# 1. 設定目標 API 網址 (請確認瀏覽器 F12 Network 中實際的資料接口)
# 這裡根據網址猜測 API 路徑，如果抓不到，請在瀏覽器查看實際 XHR 請求網址
url = "https://wpapi.ldjzmr.top/master/brand?name=&contacts=&phone=&username=&remark" 

# 2. 設定 Header (放入你提供的 Bearer Token)
headers = {
    "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczovL3dwYXBpLmxkanptci50b3AvbWFzdGVyL2xvZ2luIiwiaWF0IjoxNzY4NDYxODU1LCJleHAiOjE3OTk5OTc4NTUsIm5iZiI6MTc2ODQ2MTg1NSwianRpIjoiQnA2eEpPaHNMNjlLSkQzVCIsInN1YiI6IjEyIiwicHJ2IjoiMTg4ODk5NDM5MDUwZTVmMzc0MDliMThjYzZhNDk1NjkyMmE3YWIxYiJ9._MrYbXN4BHe4SF1lxToFzSHxN2Azlw6HjhoM6zma89Y",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json"
}

def fetch_data():
    try:
        # 3. 發送請求
        response = requests.get(url, headers=headers)
        response.raise_for_status() # 檢查請求是否成功
        
        data = response.json()
        
        # 4. 解析資料 (假設資料在 data['data']['list'] 裡，需視實際 API 結構調整)
        # 如果 API 結構不同，請調整這裡
        items = data.get('data', {}).get('list', [])
        
        if not items:
            print("未找到資料，請檢查 API 路徑或 Token 是否過期。")
            return

        # 5. 轉換為 DataFrame 並輸出 Excel
        df = pd.DataFrame(items)
        df.to_excel("brand_data.xlsx", index=False)
        print(f"成功！已抓取 {len(items)} 筆資料並儲存至 brand_data.xlsx")

    except Exception as e:
        print(f"發生錯誤: {e}")

if __name__ == "__main__":
    fetch_data()