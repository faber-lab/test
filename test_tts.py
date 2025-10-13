import os
import json
import base64
import struct

import google.generativeai as genai
from google.genai import types

from dotenv import load_dotenv

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials

# 環境変数の読み込み
load_dotenv("/etc/secrets/api.env")

# Gemini APIキー設定
genai.configure(api_key=os.getenv("Gemini_API_KEY"))

# モデル初期化
model = genai.GenerativeModel('gemini-2.5-flash-preview-tts')

# 複数話者でのテキスト
multi_speaker_text = """
田中さん: おはようございます。今日の会議の件ですが。
佐藤さん: はい、準備はできています。資料も揃えました。
田中さん: ありがとうございます。それでは10時から始めましょう。
"""

# 音声生成
response = genai.GenerativeModel("gemini-2.5-flash-preview-tts").generate_content(
    # "こんにちは。うさぎでもわかるGemini 2.5 Pro TTSの解説です。本日は宜しくお願いします。それではやっていきましょう、まずは例題から",
     multi_speaker_text,
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

def pcm_to_wav(pcm_data, sample_rate=24000, bits_per_sample=16, channels=1):
    """PCM生データをWAVファイルに変換"""
    byte_rate = sample_rate * channels * bits_per_sample // 8
    block_align = channels * bits_per_sample // 8
    data_size = len(pcm_data)
    
    header = struct.pack('<4sI4s4sIHHIIHH4sI',
        b'RIFF', data_size + 36, b'WAVE',
        b'fmt ', 16, 1, channels,
        sample_rate, byte_rate, block_align, bits_per_sample,
        b'data', data_size
    )
    
    return header + pcm_data

# 音声データを取得
part = response.candidates[0].content.parts[0]
pcm_data = part.inline_data.data
mime_type = part.inline_data.mime_type

print(f"MIME type: {mime_type}")
print(f"PCM data size: {len(pcm_data)} bytes")

# WAVに変換
wav_data = pcm_to_wav(pcm_data, sample_rate=24000, bits_per_sample=16, channels=1)

# 保存
with open("output.wav", "wb") as audio_file:
    audio_file.write(wav_data)

# 検証
with open("output.wav", "rb") as f:
    header = f.read(12)
    print(f"\n✓ WAV header: {header.hex()}")
    print(f"✓ File size: {len(wav_data)} bytes")
    print("✓ File should now be playable!")





# Google Drive API認証
SCOPES = ['https://www.googleapis.com/auth/drive.file']

CLIENT_SECRET = json.loads(os.environ["GOOGLE_CLIENT_SECRET_JSON"])
CLIENT_ID = json.loads(os.environ["GOOGLE_TOKEN_JSON"])
FOLDER_ID = os.environ["GOOGLE_DRIVE_FOLDER_ID"]


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

creds = Credentials.from_authorized_user_info(CLIENT_ID)

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
