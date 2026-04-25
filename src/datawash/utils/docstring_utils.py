import re
from typing import List

def extract_numbered_items(text: str) -> List[str]:
    pattern = r"^\d+\.(.+)$"
    matches = re.findall(pattern, text, re.MULTILINE)
    return [m.strip() for m in matches]

def extract_field_value(text: str, field_name: str) -> str:
    pattern = rf"{field_name}:\s*(.*?)(?=\n\w+:|$)"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return ""
