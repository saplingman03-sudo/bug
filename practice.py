import requests

url_list=["https://wpapi.ldjzmr.top/admin/banknote_log"]

headers = {
    "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczovL3dwYXBpLmxkanptci50b3AvYWRtaW4vbG9naW4iLCJpYXQiOjE3NzE1MzA2NTIsImV4cCI6MTgwMzA2NjY1MiwibmJmIjoxNzcxNTMwNjUyLCJqdGkiOiJDQ1cyRlhoRTV0bFNYbjFRIiwic3ViIjoiOTk5IiwicHJ2IjoiNzIzNDlhZmZkYTA0NGRjMmFkNzBhMzllZjE1MTYzZWE2N2E3MzMxMyJ9.RqU57Fn-rkRkxZuXT25wmoxDOp4HNerNMOLcA6Nt6UU",
    "Content-Type": "application/json"
}

# 發送請求，把 headers 放進去
for i in range(len(url_list)):
    r = requests.get(url_list[i], headers=headers)
    j=r.json()
    payload= None

    if "st" in j and isinstance(j["st"],dict) and "data" in j["st"]:
        payload = j["st"]["data"]["data"]

    elif "data" in j:
        if isinstance(j["data"], dict) and "data" in j["data"]:
            payload = j["data"]["data"]
        else:
            payload = j["data"]

    else:
        print("0")
        continue


    for item in payload:
        if isinstance(item, dict) and "brand_id" in item:
            print(item["brand_id"])
