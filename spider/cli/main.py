import typer

from spider.core.limits import MAX_PREVIEW_CHARS
from spider.ingest.loader import load_files

app = typer.Typer(help="Spider - CTF crypto challenge analyzer")


def make_preview(text: str, max_chars: int = MAX_PREVIEW_CHARS) -> str:
    cleaned = " ".join(text.split())
    if len(cleaned) <= max_chars:
        return cleaned
    return cleaned[:max_chars] + "..."


@app.command()
def inspect(paths: list[str]):
    """
    Inspect one or more files/directories safely without executing anything.
    """
    bundle = load_files(paths)

    print("\n=== Spider Inspect ===\n")
    print(f"Files loaded: {bundle.total_files}")
    print(f"Total size: {bundle.total_size_bytes} bytes\n")

    for item in bundle.files:
        print(f"[FILE] {item.path}")
        print(f"  Type: {item.kind}")
        print(f"  Extension: {item.extension or '(none)'}")
        print(f"  Size: {item.size_bytes} bytes")

        if item.text:
            print(f"  Preview: {make_preview(item.text)}")

        if item.notes:
            for note in item.notes:
                print(f"  Note: {note}")

        print()


if __name__ == "__main__":
    app()