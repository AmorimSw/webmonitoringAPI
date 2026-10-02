import json
import re

with open(r'C:\Users\alexandre.miranda\.gemini\antigravity-ide\brain\1aff4b2c-9335-46d5-bfe3-e14bcf70dfb2\.system_generated\steps\12\content.md', 'r', encoding='utf-8') as f:
    text = f.read()

# find blocks of json
matches = re.findall(r'\{[^{}]*"status"[^{}]*\}', text)
for m in set(matches):
    print(m)
