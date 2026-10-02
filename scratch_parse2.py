import re
import json

def extract_paths():
    with open(r'C:\Users\alexandre.miranda\.gemini\antigravity-ide\brain\1aff4b2c-9335-46d5-bfe3-e14bcf70dfb2\.system_generated\steps\12\content.md', 'r', encoding='utf-8') as f:
        text = f.read()

    matches = re.findall(r'"paths":\s*(\{.*?\})\s*,\s*"x-readme"', text, re.DOTALL)
    for m in matches:
        try:
            paths = json.loads(m)
            for path, methods in paths.items():
                print(f"Path: {path}")
                for method, details in methods.items():
                    print(f"  Method: {method}")
                    # print responses
                    if 'responses' in details:
                        for status, response in details['responses'].items():
                            print(f"    Response: {status}")
                            if 'content' in response and 'application/json' in response['content']:
                                if 'examples' in response['content']['application/json']:
                                    for ex_name, ex_val in response['content']['application/json']['examples'].items():
                                        print(f"      Example {ex_name}: {ex_val['value']}")
        except json.JSONDecodeError:
            pass

extract_paths()
