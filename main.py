import gspread
from oauth2client.service_account import ServiceAccountCredentials
from anthropic import Anthropic

import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv("/etc/secrets/api.env")  # .envファイルを読み込む

client_cla = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Google Sheets認証
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("/etc/secrets/autoyoutube-474207-e529fad13ffc.json", scope)

client_ggl = gspread.authorize(creds)

# スプレッドシートを開く
sheet = client_ggl.open("AutoYoutube").sheet1  # シート名に応じて変更
prompt = sheet.cell(2, 2).value  # B2を仮定

# Claude API からの応答を取得
response = client_cla.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1000,
    messages=[
        {"role": "user", "content": prompt}
    ]
)

#print(response.content[0].text)

# 応答内容をスプレッドシートの B3 に書き込む
sheet.update_cell(3, 2, response.content[0].text)


#-----　ここから2度目の処理　-----

# B3の内容を取得（Claudeの1回目の応答）
intermediate_text = sheet.cell(3, 2).value

# C2のプロンプトを取得
second_prompt = sheet.cell(2, 3).value  # C2 = (2, 3)

# Claude APIに再度問い合わせ（C2のプロンプト + B3の内容）
combined_prompt = f"{second_prompt}\n\n{intermediate_text}"

response2 = client_cla.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1000,
    messages=[
        {"role": "user", "content": combined_prompt}
    ]
)

# 最終応答を C3 に保存（必要に応じて変更）
final_output = response2.content[0].text
sheet.update_cell(3, 3, final_output)  

