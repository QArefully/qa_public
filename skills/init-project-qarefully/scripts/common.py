"""Shared helpers for init-project-qarefully scripts (not a CLI): UTF-8 stdio, strict text decoding, Windows
long paths, line splitting, one-line error wrapper. Loaded by file path (works under python -I); loaders set
sys.dont_write_bytecode first (no __pycache__ beside installed skill)."""
import os
import sys


class InputError(Exception):
    pass


def setup_stdio():
    """stdout/stderr -> UTF-8 (Windows pipes default to cp1252 -> UnicodeEncodeError on non-Latin paths)."""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="backslashreplace")
        except (AttributeError, ValueError, OSError):
            pass


def fs(path):
    """-> filesystem path for IO: Windows -> extended-length \\\\?\\ absolute path (no MAX_PATH 260 limit)."""
    if os.name != "nt" or path.startswith("\\\\?\\"):
        return path
    path = os.path.abspath(path)
    return "\\\\?\\UNC\\" + path[2:] if path.startswith("\\\\") else "\\\\?\\" + path


def unfs(path):
    """Inverse of fs(): extended-length prefix stripped (display, relpath against plain root)."""
    if path.startswith("\\\\?\\UNC\\"):
        return "\\\\" + path[8:]
    return path[4:] if path.startswith("\\\\?\\") else path


def decode(data, name):
    """BOM -> utf-8 / utf-16 LE|BE; NUL bytes without BOM -> InputError; else utf-8 (invalid bytes replaced)."""
    if data.startswith(b"\xef\xbb\xbf"):
        return data[3:].decode("utf-8", "replace")
    if data.startswith((b"\xff\xfe", b"\xfe\xff")):
        return data.decode("utf-16", "replace")  # BOM selects endianness, stripped
    if b"\0" in data:
        raise InputError(f"NUL bytes without BOM (binary, or UTF-16 lacking BOM): {name}")
    return data.decode("utf-8", "replace")


def read_bytes(path, name=None):
    try:
        with open(fs(path), "rb") as handle:
            return handle.read()
    except OSError as error:
        raise InputError(f"unreadable: {name or path}: {error.__class__.__name__}")


def read_text(path, name=None):
    return decode(read_bytes(path, name), name or path)


def split_lines(text):
    """-> lines split on "\\n" only (trailing "\\r" stripped); str.splitlines also splits on \\x0c, \\x1c-\\x1e,
    \\x85, U+2028/2029 -> line numbers drift from editors."""
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    return [line[:-1] if line.endswith("\r") else line for line in lines]


def one_line(error):
    text = " ".join(str(error).split())
    return f"{error.__class__.__name__}: {text}" if text else error.__class__.__name__


def guarded_main(main, argv, cleanup=None):
    """UTF-8 stdio; InputError -> "error: <msg>" exit 2; unexpected exception -> one stderr line, cleanup(), exit 2."""
    setup_stdio()
    try:
        return main(argv)
    except InputError as error:
        print(f"error: {' '.join(str(error).split())}", file=sys.stderr)
        code = 2
    except Exception as error:  # never traceback; caller treats exit 2 as blocked
        print(f"error: unexpected {one_line(error)}", file=sys.stderr)
        code = 2
    if cleanup:
        try:
            cleanup()
        except Exception:
            pass
    return code
