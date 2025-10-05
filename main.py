from anthropic import Anthropic
from config import API_KEY

client = Anthropic(api_key="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")

response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1000,
    messages=[
        {"role": "user", "content": "Hello!"}
    ]
)

print(response.content[0].text)
