import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

# 認証情報の読み込み（サービスアカウントJSONをRenderに環境変数として保存）
SERVICE_ACCOUNT_FILE = '/etc/secrets/autoyoutube-474207-e529fad13ffc.json'  # Renderでは環境変数やSecretとして扱うのが安全
SCOPES = ['https://www.googleapis.com/auth/drive']

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

# Drive APIクライアントの初期化
drive_service = build('drive', 'v3', credentials=credentials)

def create_folder(folder_name, parent_folder_id=None):
    file_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    if parent_folder_id:
        file_metadata['parents'] = [parent_folder_id]

    folder = drive_service.files().create(body=file_metadata, fields='id').execute()
    print(f"Folder '{folder_name}' created with ID: {folder.get('id')}")
    return folder.get('id')

# 使用例
if __name__ == "__main__":
    folder_id = create_folder("Renderから作ったフォルダ")
