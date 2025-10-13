import os
import google.generativeai as genai
from google.genai import types

from dotenv import load_dotenv

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# 環境変数の読み込み
load_dotenv("/etc/secrets/api.env")

# Gemini APIキー設定
genai.configure(api_key=os.getenv("Gemini_API_KEY"))

# モデル初期化
model = genai.GenerativeModel('gemini-2.5-flash-preview-tts')

# 音声生成
response = genai.GenerativeModel("gemini-2.5-flash-preview-tts").generate_content(
    "こんにちは。うさぎでもわかるGemini 2.5 Pro TTSの解説です。",
    generation_config={
        "response_modalities": ["AUDIO"],
        "speech_config": {
            "voice_config": {
                "prebuilt_voice_config": {
                    "voice_name": "kore"
                }
            }
        }
    }
)


# 音声ファイル保存
file_name = "output.wav"
with open("output.wav", "wb") as audio_file:
    audio_file.write(response.candidates[0].content.parts[0].inline_data.data)

# Google Drive API認証
SCOPES = ['https://www.googleapis.com/auth/drive.file']

CLIENT_SECRET = json.loads(os.environ["GOOGLE_CLIENT_SECRET_JSON"])
CLIENT_ID = json.loads(os.environ["GOOGLE_TOKEN_JSON"])
FOLDER_ID = os.environ("GOOGLE_DRIVE_FOLDER_ID")


flow = InstalledAppFlow.from_client_config(
    {
        "installed": {
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token"
        }
    },
    SCOPES
)

creds = flow.run_local_server(port=0)
drive_service = build('drive', 'v3', credentials=creds)

# Google Driveにアップロード
file_metadata = {
    'name': file_name,
    'parents': [FOLDER_ID]
}
media = MediaFileUpload(file_name, mimetype='audio/wav')

uploaded = drive_service.files().create(
    body=file_metadata,
    media_body=media,
    fields='id'
).execute()

print(f"✅ Google Driveにアップロード完了: File ID = {uploaded.get('id')}")
