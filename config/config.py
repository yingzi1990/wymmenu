import json
import os
from typing import Any, Dict

# 读取 JSON 文件
def load_json(file_path: str) -> Dict[str, Any]:
    try:
        with open(file_path,'r',encoding='utf-8') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' does not exist.")
        raise
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON. The file might be corrupted or contain invalid JSON.")
        raise

# 保存 JSON 文件
def save_json(file_path: str, data: dict) -> None:
    try:
        with open(file_path, 'w',encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False,indent=4)
    except IOError:
        print(f"Error: Failed to write to the file '{file_path}'.")
        raise


