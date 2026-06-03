import os

def save_to_file(code: str, file_path: str):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(code)