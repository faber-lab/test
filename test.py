import wave

from google import genai
from google.genai import types

import os
from dotenv import load_dotenv

load_dotenv("/etc/secrets/api.env")  # .envファイルを読み込む

--------------------------------------------------

import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseUpload
from io import BytesIO

class GoogleDriveUploader:
    def __init__(self, credentials_json_path=None):
        """
        Google Driveアップローダーの初期化
        
        Args:
            credentials_json_path: サービスアカウントのJSONファイルパス
                                  Noneの場合は環境変数から読み込み
        """
        SCOPES = ['https://www.googleapis.com/auth/drive.file']
        
        if credentials_json_path and os.path.exists(credentials_json_path):
            # ファイルから認証情報を読み込み
            credentials = service_account.Credentials.from_service_account_file(
                credentials_json_path, scopes=SCOPES)
        else:
            # 環境変数から認証情報を読み込み（Render推奨）
            import json
            creds_json = os.getenv('GOOGLE_CREDENTIALS_JSON')
            if not creds_json:
                raise ValueError("認証情報が見つかりません")
            
            creds_dict = json.loads(creds_json)
            credentials = service_account.Credentials.from_service_account_info(
                creds_dict, scopes=SCOPES)
        
        self.service = build('drive', 'v3', credentials=credentials)
    
    def upload_file(self, file_path, drive_folder_id=None, file_name=None):
        """
        ファイルをGoogle Driveにアップロード
        
        Args:
            file_path: アップロードするファイルのパス
            drive_folder_id: アップロード先のフォルダID（Noneの場合はルート）
            file_name: Google Drive上でのファイル名（Noneの場合は元のファイル名）
        
        Returns:
            アップロードされたファイルのID
        """
        if file_name is None:
            file_name = os.path.basename(file_path)
        
        file_metadata = {'name': file_name}
        
        if drive_folder_id:
            file_metadata['parents'] = [drive_folder_id]
        
        media = MediaFileUpload(file_path, resumable=True)
        
        file = self.service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id, name, webViewLink'
        ).execute()
        
        print(f"ファイルがアップロードされました: {file.get('name')}")
        print(f"ファイルID: {file.get('id')}")
        print(f"リンク: {file.get('webViewLink')}")
        
        return file.get('id')
    
    def upload_from_string(self, content, file_name, drive_folder_id=None, mime_type='text/plain'):
        """
        文字列データをファイルとしてGoogle Driveにアップロード
        
        Args:
            content: アップロードする文字列データ
            file_name: Google Drive上でのファイル名
            drive_folder_id: アップロード先のフォルダID
            mime_type: ファイルのMIMEタイプ
        
        Returns:
            アップロードされたファイルのID
        """
        file_metadata = {'name': file_name}
        
        if drive_folder_id:
            file_metadata['parents'] = [drive_folder_id]
        
        # 文字列をバイトストリームに変換
        fh = BytesIO(content.encode('utf-8'))
        media = MediaIoBaseUpload(fh, mimetype=mime_type, resumable=True)
        
        file = self.service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id, name, webViewLink'
        ).execute()
        
        print(f"ファイルがアップロードされました: {file.get('name')}")
        print(f"ファイルID: {file.get('id')}")
        
        return file.get('id')
    
    def create_folder(self, folder_name, parent_folder_id=None):
        """
        Google Drive上にフォルダを作成
        
        Args:
            folder_name: 作成するフォルダ名
            parent_folder_id: 親フォルダID（Noneの場合はルート）
        
        Returns:
            作成されたフォルダのID
        """
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        
        if parent_folder_id:
            file_metadata['parents'] = [parent_folder_id]
        
        folder = self.service.files().create(
            body=file_metadata,
            fields='id, name'
        ).execute()
        
        print(f"フォルダが作成されました: {folder.get('name')}")
        print(f"フォルダID: {folder.get('id')}")
        
        return folder.get('id')

--------------------------------------------------

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


