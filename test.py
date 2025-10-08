import wave

from google import genai
from google.genai import types

import os
from dotenv import load_dotenv

load_dotenv("/etc/secrets/api.env")  # .envファイルを読み込む

# Set up the wave file to save the output:
def wave_file(filename, pcm, channels=1, rate=24000, sample_width=2):
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(rate)
        wf.writeframes(pcm)


client = genai.Client(
    api_key=os.getenv("Gemini_API_KEY")
)  # Gemini APIキーを設定してください

# client_cla = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

response = client.models.generate_content(
    model='gemini-2.5-flash-preview-tts',
    contents='Say cheerfully: Have a wonderful day!',
    config=types.GenerateContentConfig(
        response_modalities=['AUDIO'],
        speech_config=types.SpeechConfig(
            voice_config=types.VoiceConfig(
                prebuilt_voice_config=types.PrebuiltVoiceConfig(
                    voice_name='Kore',
                )
            )
        ),
    ),
)

data = response.candidates[0].content.parts[0].inline_data.data

file_name = 'out.wav'
wave_file(file_name, data)  # Saves the file to current directory


from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# 認証情報の読み込み
SCOPES = ['https://www.googleapis.com/auth/drive.file']
SERVICE_ACCOUNT_FILE = '/etc/secrets/autoyoutube-474207-e529fad13ffc.json'  # JSONキーのパス

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

drive_service = build('drive', 'v3', credentials=credentials)

# Google Driveにアップロード
file_metadata = {
    'name': file_name,
    # 'parents': ['your_folder_id']  # フォルダ指定する場合はここにIDを入れる
}
media = MediaFileUpload(file_name, mimetype='audio/wav')

uploaded = drive_service.files().create(
    body=file_metadata,
    media_body=media,
    fields='id'
).execute()

print(f"Uploaded to Google Drive with file ID: {uploaded.get('id')}")

