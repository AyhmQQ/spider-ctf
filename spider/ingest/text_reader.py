from typing import Optional


def read_text(raw_bytes: bytes) -> Optional[str]:
    try:
        return raw_bytes.decode("utf-8", errors="ignore")
    except Exception:
        return None