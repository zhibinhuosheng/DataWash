import os
from typing import List

def read_file(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def resolve_path(base: str, relative: str) -> str:
    return os.path.join(base, relative)

def write_json(file_path: str, data: dict) -> None:
    import json
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def list_json_files(directory: str) -> List[str]:
    result = []
    for f in os.listdir(directory):
        if f.endswith(".json"):
            result.append(os.path.join(directory, f))
    return sorted(result)
