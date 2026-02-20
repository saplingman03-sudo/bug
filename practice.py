import requests

url_list=["https://wpapi.ldjzmr.top/admin/banknote/brand_info","https://wpapi.ldjzmr.top/admin/banknote_log","https://wpapi.ldjzmr.top/admin/machine","https://wpapi.ldjzmr.top/admin/banknote/brand_info"]

headers = {
    "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczovL3dwYXBpLmxkanptci50b3AvYWRtaW4vbG9naW4iLCJpYXQiOjE3NzE1MzA2NTIsImV4cCI6MTgwMzA2NjY1MiwibmJmIjoxNzcxNTMwNjUyLCJqdGkiOiJDQ1cyRlhoRTV0bFNYbjFRIiwic3ViIjoiOTk5IiwicHJ2IjoiNzIzNDlhZmZkYTA0NGRjMmFkNzBhMzllZjE1MTYzZWE2N2E3MzMxMyJ9.RqU57Fn-rkRkxZuXT25wmoxDOp4HNerNMOLcA6Nt6UU",
    "Content-Type": "application/json"
}

# 發送請求，把 headers 放進去
for url in url_list:
    response = requests.get(url, headers=headers)
    print(response.text)