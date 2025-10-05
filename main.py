from anthropic import Anthropic

import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv("/etc/secrets/api.env")  # .envファイルを読み込む

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1000,
    messages=[
        {"role": "user", "content": "Hello!"}
    ]
)

print(response.content[0].text)
