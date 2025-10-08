import wave

from google import genai
from google.genai import types

import os
from dotenv import load_dotenv

load_dotenv("/etc/secrets/api.env")  # .envファイルを読み込む

from google_drive_uploader import GoogleDriveUploader

# 初期化
uploader = GoogleDriveUploader()

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
# wave_file(file_name, data)  # Saves the file to current directory

# 特定のフォルダにアップロード
file_id = uploader.upload_file('out.wav', drive_folder_id='0AGktFDT2dCBRUk9PVA')


