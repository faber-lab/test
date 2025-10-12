import os
import io
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

# --- 環境変数から認証情報を読み込む ---
client_secret_info = json.loads(os.environ["GOOGLE_CLIENT_SECRET_JSON"])
token_info = json.loads(os.environ["GOOGLE_TOKEN_JSON"])
folder_id = os.environ["GOOGLE_DRIVE_FOLDER_ID"]

# --- 認証 ---
creds = Credentials.from_authorized_user_info(token_info)

# --- Drive API 初期化 ---
service = build("drive", "v3", credentials=creds)

# --- アップロードファイル設定 ---
file_name = "render_upload_test.txt"
file_content = "Hello from Render via OAuth!"
file_metadata = {
    "name": file_name,
    "parents": [folder_id],
}

media = MediaIoBaseUpload(io.BytesIO(file_content.encode("utf-8")), mimetype="text/plain")

# --- ファイルアップロード ---
uploaded_file = service.files().create(
    body=file_metadata,
    media_body=media,
    fields="id, name"
).execute()

print(f"✅ Uploaded: {uploaded_file['name']} (ID: {uploaded_file['id']})")
