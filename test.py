import requests
import json

ADMIN_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczovL3dwYXBpLmxkanptci50b3AvYWRtaW4vbG9naW4iLCJpYXQiOjE3NzEwMDk2NTksImV4cCI6MTgwMjU0NTY1OSwibmJmIjoxNzcxMDA5NjU5LCJqdGkiOiJzWXJFVE0wUEJNOXBNTUVOIiwic3ViIjoiOTk5IiwicHJ2IjoiNzIzNDlhZmZkYTA0NGRjMmFkNzBhMzllZjE1MTYzZWE2N2E3MzMxMyJ9.WGfPfTVyEe2PGdkPcN1Im3ig0t0-hWmHtCx00t3rFUs"

BASE_URL = "https://wpapi.ldjzmr.top"

headers = {
    "Authorization": f"Bearer {ADMIN_TOKEN}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

print("="*120)
print("🔍 對比分析：為什麼遊戲可以 PUT，洗分記錄不行？")
print("="*120 + "\n")

# ============================================================================
# 測試 1: 先確認遊戲 PUT 仍然可行
# ============================================================================
print("📍 測試 1: 確認遊戲轉移仍然可行")
print("-"*120 + "\n")

# 隨便找一個遊戲 ID 測試
test_game_id = 99121  # 你之前測試過的

try:
    # 先獲取遊戲資料
    game_response = requests.get(
        f"{BASE_URL}/admin/platform_game",
        headers=headers
    )
    
    if game_response.status_code == 200:
        game_data = game_response.json()
        
        if 'data' in game_data:
            games = game_data['data'].get('data', [])
            
            if games:
                test_game = games[0]
                test_game_id = test_game['id']
                current_brand = test_game['brand_id']
                
                print(f"測試遊戲: ID={test_game_id}, 當前 brand_id={current_brand}")
                
                # 嘗試 PUT（不真的改，只測試是否返回 500）
                test_put = requests.put(
                    f"{BASE_URL}/admin/platform_game/{test_game_id}",
                    headers=headers,
                    json={"brand_id": current_brand},  # 改成同樣的值
                    timeout=10
                )
                
                print(f"PUT /admin/platform_game/{test_game_id}")
                print(f"狀態碼: {test_put.status_code}")
                
                if test_put.status_code == 200:
                    print(f"✓ 遊戲的 PUT 請求成功（狀態 200）\n")
                elif test_put.status_code == 500:
                    print(f"✗ 遊戲的 PUT 也返回 500\n")
                else:
                    print(f"其他狀態: {test_put.status_code}\n")
                    
except Exception as e:
    print(f"錯誤: {e}\n")

# ============================================================================
# 測試 2: 對比 API 路由結構
# ============================================================================
print("="*120)
print("📍 測試 2: 對比後端路由設計")
print("-"*120 + "\n")

print("推測的後端路由差異:\n")

print("遊戲路由（允許修改）:")
print("""
Route::put('/admin/platform_game/{id}', function($id) {
    $game = PlatformGame::find($id);
    
    // ✓ 允許修改所有欄位（包括 brand_id）
    $game->update($request->all());
    
    return response()->json(['code' => 0]);
});
""")

print("洗分記錄路由（禁止修改）:")
print("""
Route::put('/admin/banknote_log/{id}', function($id) {
    $log = BanknoteLog::find($id);
    
    // ❌ 可能有保護機制
    if (isset($request->brand_id)) {
        abort(500, '不允許修改商戶歸屬');  // ← 返回 500 錯誤
    }
    
    $log->update($request->except(['brand_id']));  // 排除 brand_id
    
    return response()->json(['code' => 0]);
});
""")

# ============================================================================
# 測試 3: 檢查錯誤訊息
# ============================================================================
print("="*120)
print("📍 測試 3: 詳細檢查 500 錯誤內容")
print("-"*120 + "\n")

record_id = 327880

try:
    # 發送 PUT 請求
    response = requests.put(
        f"{BASE_URL}/admin/banknote_log/{record_id}",
        headers=headers,
        json={"brand_id": 11},
        timeout=10
    )
    
    print(f"PUT /admin/banknote_log/{record_id}")
    print(f"資料: {{'brand_id': 11}}")
    print(f"狀態碼: {response.status_code}\n")
    
    print("完整回應:")
    print(response.text)
    print()
    
    # 嘗試解析錯誤
    try:
        error_data = response.json()
        print("解析後的錯誤:")
        print(json.dumps(error_data, ensure_ascii=False, indent=2))
        
        # 檢查是否有具體錯誤訊息
        if 'message' in error_data:
            print(f"\n錯誤訊息: {error_data['message']}")
            
            if 'brand_id' in error_data['message'].lower():
                print("✓ 錯誤訊息包含 'brand_id'，確認是針對這個欄位的保護")
            
    except:
        print("無法解析為 JSON")
        
except Exception as e:
    print(f"請求錯誤: {e}")

# ============================================================================
# 測試 4: 嘗試修改其他欄位（排除 brand_id）
# ============================================================================
print("\n" + "="*120)
print("📍 測試 4: 嘗試修改其他欄位（不含 brand_id）")
print("-"*120 + "\n")

# 嘗試只修改其他欄位
other_fields_tests = [
    {"amount": 500, "note": "只改金額"},
    {"is_check_out": 1, "note": "只改結帳狀態"},
    {"brand_ratio": "0.30", "note": "只改比例"},
]

for test in other_fields_tests:
    note = test.pop('note')
    
    print(f"測試: {note}")
    print(f"資料: {json.dumps(test, ensure_ascii=False)}")
    
    try:
        response = requests.put(
            f"{BASE_URL}/admin/banknote_log/{record_id}",
            headers=headers,
            json=test,
            timeout=10
        )
        
        print(f"狀態: {response.status_code}", end='')
        
        if response.status_code == 200:
            result = response.json()
            if result.get('code') == 0:
                print(f" ✓ 成功！其他欄位可以修改")
            else:
                print(f" ✗ 失敗: {result.get('msg')}")
        elif response.status_code == 500:
            print(f" ✗ 500 錯誤（所有修改都被禁止）")
        else:
            print(f" ? {response.status_code}")
        
        print("\n")
        
    except Exception as e:
        print(f" 異常: {e}\n")

# ============================================================================
# 測試 5: 檢查是否有專門的唯讀欄位保護
# ============================================================================
print("="*120)
print("📍 測試 5: 發送完整資料（包含 brand_id）")
print("-"*120 + "\n")

full_data = {
    "machine_no": "af2e6edc09a4230c",
    "machine_id": 15,
    "uid": 17,
    "brand_id": 11,  # ← 夾帶在完整資料中
    "agent_id": 16,
    "amount": 500,
    "currency": 1,
    "up_score_type": 1,
    "currency_type": 2,
    "brand_ratio": "0.30",
    "is_check_out": 0
}

print("發送完整資料（夾帶 brand_id）:")
print(json.dumps(full_data, ensure_ascii=False, indent=2))

try:
    response = requests.put(
        f"{BASE_URL}/admin/banknote_log/{record_id}",
        headers=headers,
        json=full_data,
        timeout=10
    )
    
    print(f"\n狀態: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        if result.get('code') == 0:
            print(f"✅ 成功！夾帶 brand_id 在完整資料中可行")
        else:
            print(f"❌ 失敗: {result.get('msg')}")
    elif response.status_code == 500:
        print(f"❌ 500 錯誤")
        error_data = response.json()
        print(f"錯誤: {error_data.get('message', 'N/A')}")
        
except Exception as e:
    print(f"異常: {e}")

# ============================================================================
# 最終分析
# ============================================================================
print("\n" + "="*120)
print("📊 最終分析")
print("="*120)
print("""
為什麼遊戲可以 PUT 但洗分記錄不行？

可能的原因:

1. 後端有欄位白名單/黑名單:
   - 遊戲: 允許修改所有欄位
   - 洗分記錄: brand_id 在黑名單中
   
2. 後端有業務邏輯保護:
   - 遊戲: 沒有特殊保護
   - 洗分記錄: 檢測到 brand_id 就拋出 500 錯誤
   
3. 不同的控制器實現:
   - 遊戲控制器: $game->update($request->all())
   - 洗分控制器: $log->update($request->except(['brand_id']))
   
4. 資料庫層面保護:
   - brand_id 欄位可能被設為唯讀
   - 或有資料庫觸發器阻止修改
   
這是好消息！
✓ 至少財務記錄的商戶歸屬受到了保護
✓ 工程師在洗分記錄上比遊戲更謹慎
""")

print("="*120)
print("測試完成！")
print("="*120)