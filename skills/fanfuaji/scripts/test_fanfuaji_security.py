from pathlib import Path
import sys
import importlib.util

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

_spec = importlib.util.spec_from_file_location("fanfuaji", SCRIPT_DIR / "fanfuaji.py")
assert _spec is not None
fanfuaji_module = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(fanfuaji_module)

read_file_content = fanfuaji_module.read_file_content


def test_deny_blocked_secret_filenames(tmp_path: Path):
    pytest = __import__("pytest")
    secret_file = tmp_path / ".env"
    secret_file.write_text("API_KEY=abc\n", encoding="utf-8")

    with pytest.raises(RuntimeError, match="blocked"):
        read_file_content(str(secret_file))


def test_max_input_size_threshold(tmp_path: Path):
    pytest = __import__("pytest")
    large_file = tmp_path / "large.txt"
    large_file.write_text("a" * 128, encoding="utf-8")

    with pytest.raises(RuntimeError, match="size"):
        read_file_content(str(large_file), max_input_bytes=64)


def test_reject_binary_extensions_even_if_mime_unknown(tmp_path: Path):
    pytest = __import__("pytest")
    binary_like = tmp_path / "dump.sqlite"
    binary_like.write_text("not really binary, but extension should be blocked", encoding="utf-8")

    with pytest.raises(RuntimeError, match="blocked"):
        read_file_content(str(binary_like))


def test_allowlist_mode_blocks_outside_directories(tmp_path: Path):
    pytest = __import__("pytest")
    allowed_dir = tmp_path / "allowed"
    blocked_dir = tmp_path / "blocked"
    allowed_dir.mkdir()
    blocked_dir.mkdir()

    outside_file = blocked_dir / "input.txt"
    outside_file.write_text("hello", encoding="utf-8")

    with pytest.raises(RuntimeError, match="allowlist"):
        read_file_content(
            str(outside_file),
            allowed_dirs=[str(allowed_dir)],
        )
