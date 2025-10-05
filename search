import gspread
from oauth2client.service_account import ServiceAccountCredentials
import anthropic

# Google Sheets認証
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("your_google_credentials.json", scope)
client = gspread.authorize(creds)

# スプレッドシートを開く
sheet = client.open("ClaudeTasks").sheet1  # シート名に応じて変更

# プロンプトを読み込む（例：A列にプロンプトがある）
prompts = sheet.col_values(1)[1:]  # 1行目はヘッダーと仮定

# Claude API設定
claude = anthropic.Anthropic(api_key="YOUR_ANTHROPIC_API_KEY")

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
