from google.oauth2 import service_account
from googleapiclient.discovery import build
import io
from googleapiclient.http import MediaIoBaseUpload

# --- 設定 ---
SERVICE_ACCOUNT_FILE = "/etc/secrets/client_secret_599500399129-nqah0dbjj0ikk8l2r17304gr1l2ombdm.apps.googleusercontent.com.json"  # Render上に置く or 環境変数で読み込む
SCOPES = ["https://www.googleapis.com/auth/drive.file"]
FOLDER_ID = "1BT8_ri8ukTlyahgDpWVHY6QDXH6s7JBy"  # アップロード先のフォルダID

# --- 認証 ---
creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

# --- Drive API 初期化 ---
service = build("drive", "v3", credentials=creds)

# --- アップロードするファイル情報 ---
file_name = "example.txt"
file_content = "Hello from Render!"

file_metadata = {
    "name": file_name,
    "parents": [FOLDER_ID]  # フォルダIDを指定
}

media = MediaIoBaseUpload(io.BytesIO(file_content.encode("utf-8")),
                          mimetype="text/plain")

# --- アップロード実行 ---
uploaded_file = service.files().create(
    body=file_metadata,
    media_body=media,
    fields="id"
).execute()

print(f"✅ File uploaded successfully: {uploaded_file.get('id')}")
