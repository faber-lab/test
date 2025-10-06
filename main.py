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
prompts = sheet.cell(2, 2).value  # B2を仮定

response = client_cla.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1000,
    messages=[
        {"role": "user", "content": prompt}
    ]
)

print(response.content[0].text)
