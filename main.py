pip install -U anthropic
from anthropic import Anthropic

client = Anthropic(api_key="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")

response = client.messages.create(
    model="claude-3-opus-20240229",
    messages=[
        {"role": "user", "content": "Hello!"}
    ]
)

print(response.content[0].text)
