from pathlib import Path

from spider.core.limits import MAX_FILE_SIZE_BYTES, MAX_FILES_IN_DIRECTORY
from spider.models.challenge_bundle import ChallengeBundle
from spider.models.input_file import InputFile

from .file_classifier import classify_file
from .text_reader import read_text


def load_files(paths: list[str]) -> ChallengeBundle:
    bundle = ChallengeBundle()

    for raw_path in paths:
        path = Path(raw_path)

        if not path.exists():
            continue

        if path.is_file():
            processed = process_file(path)
            if processed is not None:
                bundle.add_file(processed)

        elif path.is_dir():
            count = 0
            for file_path in sorted(path.rglob("*")):
                if not file_path.is_file():
                    continue

                count += 1
                if count > MAX_FILES_IN_DIRECTORY:
                    break

                processed = process_file(file_path)
                if processed is not None:
                    bundle.add_file(processed)

    return bundle


def process_file(path: Path) -> InputFile | None:
    try:
        size = path.stat().st_size
    except OSError:
        return None

    if size > MAX_FILE_SIZE_BYTES:
        return InputFile(
            path=path,
            extension=path.suffix.lower(),
            kind="skipped",
            size_bytes=size,
            raw_bytes=b"",
            text=None,
            notes=[f"Skipped: file exceeds {MAX_FILE_SIZE_BYTES} bytes"],
        )

    try:
        raw = path.read_bytes()
    except OSError:
        return InputFile(
            path=path,
            extension=path.suffix.lower(),
            kind="unreadable",
            size_bytes=size,
            raw_bytes=b"",
            text=None,
            notes=["Could not read file contents"],
        )

    kind = classify_file(path, raw)

    text = None
    notes: list[str] = []

    if kind in {"text", "python_source", "key_material"}:
        text = read_text(raw)
        if text is None:
            notes.append("Text decoding failed")
    else:
        notes.append("Binary content detected")

    return InputFile(
        path=path,
        extension=path.suffix.lower(),
        kind=kind,
        size_bytes=size,
        raw_bytes=raw,
        text=text,
        notes=notes,
    )