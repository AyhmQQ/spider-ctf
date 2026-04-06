from pathlib import Path


TEXT_EXTENSIONS = {
    ".txt", ".log", ".out", ".md", ".csv", ".yaml", ".yml", ".json"
}

PYTHON_EXTENSIONS = {
    ".py", ".sage"
}

KEY_EXTENSIONS = {
    ".pem", ".der", ".pub", ".key", ".crt", ".cer"
}

BINARY_HINT_EXTENSIONS = {
    ".enc", ".bin", ".dat", ".raw"
}


def looks_like_text(raw_bytes: bytes, sample_size: int = 2048) -> bool:
    sample = raw_bytes[:sample_size]
    if not sample:
        return True

    # إذا فيه null bytes غالبًا binary
    if b"\x00" in sample:
        return False

    try:
        sample.decode("utf-8")
        return True
    except UnicodeDecodeError:
        return False


def classify_file(path: Path, raw_bytes: bytes) -> str:
    ext = path.suffix.lower()

    if ext in PYTHON_EXTENSIONS:
        return "python_source"

    if ext in KEY_EXTENSIONS:
        return "key_material"

    if ext in TEXT_EXTENSIONS:
        return "text"

    if ext in BINARY_HINT_EXTENSIONS:
        return "binary" if not looks_like_text(raw_bytes) else "text"

    return "text" if looks_like_text(raw_bytes) else "binary"