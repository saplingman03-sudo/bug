import requests
import pandas as pd
import time
import sys

# API 基礎配置
base_url = "https://wpapi.ldjzmr.top/master/brand"
headers = {
    "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczovL3dwYXBpLmxkanptci50b3AvbWFzdGVyL2xvZ2luIiwiaWF0IjoxNzY4NDYxODU1LCJleHAiOjE3OTk5OTc4NTUsIm5iZiI6MTc2ODQ2MTg1NSwianRpIjoiQnA2eEpPaHNMNjlLSkQzVCIsInN1YiI6IjEyIiwicHJ2IjoiMTg4ODk5NDM5MDUwZTVmMzc0MDliMThjYzZhNDk1NjkyMmE3YWIxYiJ9._MrYbXN4BHe4SF1lxToFzSHxN2Azlw6HjhoM6zma89Y",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def fetch_dynamic_all():
    all_items = []
    page = 1
    total_target = None # 初始設為未知
    
    print("🔍 正在初始化並確認資料總數...")

    while True:
        params = {"page": page}
        
        try:
            response = requests.get(base_url, headers=headers, params=params)
            response.raise_for_status()
            res_json = response.json()
            
            # 從 API 第一頁回傳的資訊中自動抓取『最新總數』
            data_obj = res_json.get('data', {})
            
            # 如果是第一次執行，從回傳資料中抓取總數
            if total_target is None:
                if isinstance(data_obj, dict):
                    total_target = data_obj.get('total', 0)
                else:
                    # 如果結構比較簡單，就嘗試從目前的列表長度判斷（或是先預設一個大數字）
                    total_target = 9999 
                print(f"📈 偵測到系統當前共有 {total_target} 筆資料，準備開始抓取...\n")

            # 提取當前頁面的列表
            current_list = data_obj.get('data', []) if isinstance(data_obj, dict) else data_obj
            
            if not current_list:
                break
            
            all_items.extend(current_list)
            
            # 即時進度顯示
            current_count = len(all_items)
            percent = (current_count / total_target) * 100 if total_target > 0 else 0
            
            sys.stdout.write(f"\r正在抓取：第 {page:2d} 頁 | 進度: [{'#' * (int(percent//5))}{'.' * (20 - int(percent//5))}] {percent:.1f}% ({current_count}/{total_target})")
            sys.stdout.flush()
            
            # 判斷是否已經抓完
            if current_count >= total_target:
                break
                
            page += 1
            time.sleep(0.2)
            
        except Exception as e:
            print(f"\n❌ 錯誤: {e}")
            break

    if all_items:
        print(f"\n\n✅ 抓取完成！實際抓取：{len(all_items)} 筆")
        df = pd.DataFrame(all_items)
        df.to_excel("最新全量品牌資料.xlsx", index=False)
        print("📁 檔案已儲存：最新全量品牌資料.xlsx")
    else:
        print("\n❌ 未抓取到資料。")

if __name__ == "__main__":
    fetch_dynamic_all()