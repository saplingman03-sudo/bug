import requests
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

BASE_URL = "https://wpapi.ldjzmr.top"

print("="*120)
print("⚠️  溫和壓力測試（僅用於評估，不造成實際攻擊）")
print("="*120 + "\n")

# 測試參數（非常保守）
CONCURRENT_USERS = 5  # 只模擬 5 個並發用戶
REQUESTS_PER_USER = 10  # 每個用戶發 10 個請求
DELAY_BETWEEN_REQUESTS = 0.5  # 每個請求間隔 0.5 秒

print(f"測試參數:")
print(f"  並發用戶: {CONCURRENT_USERS}")
print(f"  每人請求數: {REQUESTS_PER_USER}")
print(f"  請求間隔: {DELAY_BETWEEN_REQUESTS} 秒")
print(f"  總請求數: {CONCURRENT_USERS * REQUESTS_PER_USER}")
print(f"  預計耗時: ~{REQUESTS_PER_USER * DELAY_BETWEEN_REQUESTS:.0f} 秒\n")

response_times = []
errors = 0
success = 0

def user_simulation(user_id):
    """模擬單個用戶的行為"""
    global errors, success
    
    for i in range(REQUESTS_PER_USER):
        try:
            start_time = time.time()
            
            # 隨機訪問不同端點（模擬真實用戶）
            endpoints = [
                "/admin/brand/11",
                "/admin/brand/12",
                "/agent/agent/16",
            ]
            
            endpoint = endpoints[i % len(endpoints)]
            
            response = requests.get(
                f"{BASE_URL}{endpoint}",
                timeout=5
            )
            
            end_time = time.time()
            response_time = (end_time - start_time) * 1000  # 轉成毫秒
            
            response_times.append(response_time)
            
            if response.status_code == 200:
                success += 1
            else:
                errors += 1
            
            print(f"用戶 {user_id} 請求 {i+1}: {response.status_code} ({response_time:.0f}ms)")
            
            time.sleep(DELAY_BETWEEN_REQUESTS)
            
        except Exception as e:
            errors += 1
            print(f"用戶 {user_id} 請求 {i+1}: 錯誤 ({str(e)[:30]})")

# 執行測試
print("開始測試...\n")
start_time = time.time()

with ThreadPoolExecutor(max_workers=CONCURRENT_USERS) as executor:
    futures = [executor.submit(user_simulation, i) for i in range(1, CONCURRENT_USERS + 1)]
    
    for future in futures:
        future.result()

end_time = time.time()
total_time = end_time - start_time

# 統計結果
print("\n" + "="*120)
print("📊 測試結果")
print("="*120 + "\n")

print(f"總請求數: {len(response_times) + errors}")
print(f"成功: {success}")
print(f"失敗: {errors}")
print(f"總耗時: {total_time:.2f} 秒")
print(f"平均 QPS: {(success + errors) / total_time:.2f} 請求/秒\n")

if response_times:
    avg_response = sum(response_times) / len(response_times)
    min_response = min(response_times)
    max_response = max(response_times)
    
    print(f"回應時間統計:")
    print(f"  平均: {avg_response:.0f} ms")
    print(f"  最快: {min_response:.0f} ms")
    print(f"  最慢: {max_response:.0f} ms")

print("\n" + "="*120)
print("💡 結論")
print("="*120)
print(f"""
這只是 {CONCURRENT_USERS} 個並發用戶的溫和測試。

如果要進行 DDoS:
  - 並發數: 100-1000 個執行緒
  - 持續時間: 數分鐘到數小時
  - 無延遲: 瘋狂發送請求
  
預估效果:
  {'🟢 伺服器可能撐得住' if avg_response < 1000 and errors == 0 else ''}
  {'🟡 伺服器可能會變慢' if 1000 <= avg_response < 3000 else ''}
  {'🔴 伺服器可能會崩潰' if avg_response >= 3000 or errors > 0 else ''}
  
真實 DDoS 會造成:
  🔴 API 完全無法回應
  🔴 所有用戶無法登入
  🔴 平台完全癱瘓
  🔴 可能需要數小時才能恢復
""")

print("="*120)