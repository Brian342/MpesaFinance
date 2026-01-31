"""Installable copy of the imghdr shim.
"""
from typing import Optional


def _read_header(file) -> bytes:
    try:
        if hasattr(file, "read"):
            pos = None
            try:
                pos = file.tell()
            except Exception:
                pos = None
            header = file.read(32)
            if pos is not None:
                try:
                    file.seek(pos)
                except Exception:
                    pass
            return header
        else:
            with open(file, "rb") as f:
                return f.read(32)
    except Exception:
        return b""


def what(file, h: Optional[bytes] = None) -> Optional[str]:
    if h is None:
        h = _read_header(file)[:32]
    else:
        h = h[:32]

    if not h:
        return None

    if h[:2] == b"\xff\xd8":
        return "jpeg"
    if h.startswith(b"\x89PNG\r\n\x1a\n"):
        return "png"
    if h.startswith(b"GIF87a") or h.startswith(b"GIF89a"):
        return "gif"
    if h[:2] == b"BM":
        return "bmp"
    if h.startswith(b"II*") or h.startswith(b"MM\x00*"):
        return "tiff"
    if h.startswith(b"RIFF") and h[8:12] == b"WEBP":
        return "webp"
    if h[:4] == b"\x00\x00\x01\x00":
        return "ico"
    return None

__all__ = ["what"]
