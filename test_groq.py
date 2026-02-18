import os
from groq import Groq

api_key = "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"

print(f"Testing key: {api_key}")
print(f"Key length: {len(api_key)}")

client = Groq(api_key=api_key)

try:
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": "Hello"
            }
        ],
        temperature=0.7,
        max_tokens=10
    )
    print("Success!")
    print(completion.choices[0].message.content)
except Exception as e:
    print(f"Error: {e}")
