import os
from pathlib import Path
from typing import Tuple

STORAGE_ROOT = Path(os.getenv("DATA_STORAGE_ROOT", "./data_storage"))

def ensure_year_dir(year: int):
    d = STORAGE_ROOT / str(year)
    d.mkdir(parents=True, exist_ok=True)
    return d

def save_upload_file(upload_file, year: int, filename: str) -> Tuple[str,int]:
    dest_dir = ensure_year_dir(year)
    dest_path = dest_dir / filename
    if dest_path.exists():
        from time import time
        dest_path = dest_dir / f"{int(time())}_{filename}"
    with open(dest_path, "wb") as f:
        while True:
            chunk = upload_file.file.read(1024*1024)
            if not chunk:
                break
            f.write(chunk)
    size = dest_path.stat().st_size
    return str(dest_path), size
