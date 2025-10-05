import gspread
from oauth2client.service_account import ServiceAccountCredentials
import anthropic

# Google Sheets認証
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("autoyoutube-474207-5aba7833ff63.json", scope)
client = gspread.authorize(creds)

# スプレッドシートを開く
#sheet = client.open("AutoYoutube").sheet1  # シート名に応じて変更

# プロンプトを読み込む（例：A列にプロンプトがある）
#prompts = sheet.cell(2, 3).value  # C2を仮定
prompts = "自己紹介をして下さい"

# Claude API設定
claude = Anthropic(api_key="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")

# Claudeでタスク実行
for i, prompt in enumerate(prompts):
    response = claude.messages.create(
        model="claude-2.1",
        max_tokens=1000,
        temperature=0.7,
        messages=[{"role": "user", "content": prompt}]
    )
    result = response.content

    # 結果をB列に書き込み
    sheet.update_cell(i + 2, 2, result)  # 2行目から開始（ヘッダー除く）
