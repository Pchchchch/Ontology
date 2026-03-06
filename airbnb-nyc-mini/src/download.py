###역할: URL에서 파일을 다운로드하고 진행률 표시(tqdm).

from pathlib import Path
import requests
from tqdm import tqdm

def download_file(url: str, out_path: Path, overwrite: bool = False) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if out_path.exists() and not overwrite:
        print(f"[skip] {out_path.name} already exists")
        return

    headers = {"User-Agent": "Mozilla/5.0"}

    with requests.get(url, stream=True, timeout=60, headers=headers) as r:
        r.raise_for_status()
        total = int(r.headers.get("content-length", 0))
        with open(out_path, "wb") as f, tqdm(total=total, unit="B", unit_scale=True) as pbar:
            for chunk in r.iter_content(chunk_size=1024 * 256):
                if chunk:
                    f.write(chunk)
                    pbar.update(len(chunk))
    print(f"[ok] downloaded -> {out_path}")