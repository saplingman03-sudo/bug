import pandas as pd
from playwright.sync_api import sync_playwright

API_URL = "https://wpadmin.ldjzmr.top"  # TODO: 換成你 Network 看到的表格 API
STATE_FILE = "state.json"

def fetch_all_merchants():
    rows_all = []
    page_num = 1
    page_size = 50

    with sync_playwright() as p:
        ctx = p.chromium.launch().new_context(storage_state=STATE_FILE)
        request = ctx.request

        while True:
            params = {
                "pageNum": page_num,
                "pageSize": page_size,
                # TODO: 你的篩選條件也加在這
                # "merchantName": "",
                # "linkMan": "",
                # "startDate": "",
                # "endDate": "",
            }

            r = request.get(API_URL, params=params)
            data = r.json()

            # TODO: 依你的 API 結構調整
            rows = data["data"]["rows"]
            total = data["data"]["total"]

            rows_all.extend(rows)

            if len(rows_all) >= total or not rows:
                break

            page_num += 1

    return rows_all

def export_excel(rows, filename="商戶管理.xlsx"):
    df = pd.DataFrame(rows)

    # ✅ 你可以做欄位重命名，變成你想要的 Excel 標題
    rename_map = {
        "id": "ID",
        "merchantName": "商戶名稱",
        "machineCount": "機器數量",
        "address": "商戶地址",
        "agent": "所屬代理",
        "contact": "聯繫人",
        "loginAccount": "登錄帳號",
        "shareRate": "分成[%]",
        "onceMin": "單次開分金額",
        "minWash": "最低洗分金額",
        "bet": "投鈔",
        "open": "開分",
        "wash": "洗分",
        "balance": "盈餘",
        "createdAt": "創建日",
    }
    df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})

    df.to_excel(filename, index=False)

if __name__ == "__main__":
    rows = fetch_all_merchants()
    export_excel(rows)
