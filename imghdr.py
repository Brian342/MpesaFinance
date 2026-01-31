"""
Lightweight replacement for the stdlib `imghdr` module for environments
where it's unavailable (e.g., Python 3.13 removal). Implements a minimal
`what()` function used by Streamlit to detect common image types.

This file lives at project root so `import imghdr` will find it before
the (missing) stdlib module in the deployed environment.
"""
from __future__ import annotations

from typing import Optional


def _read_header(file) -> bytes:
    # `file` may be a filename (str/bytes/Path) or file-like object.
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
    """Return a string describing the image type, or None.

    Recognizes: jpeg, png, gif, bmp, tiff, webp, ico
    """
    if h is None:
        h = _read_header(file)[:32]
    else:
        h = h[:32]

    if not h:
        return None

    # JPEG
    if h[:2] == b"\xff\xd8":
        return "jpeg"

    # PNG
    if h.startswith(b"\x89PNG\r\n\x1a\n"):
        return "png"

    # GIF
    if h.startswith(b"GIF87a") or h.startswith(b"GIF89a"):
        return "gif"

    # BMP
    if h[:2] == b"BM":
        return "bmp"

    # TIFF (II or MM)
    if h.startswith(b"II*") or h.startswith(b"MM\x00*"):
        return "tiff"

    # WEBP (RIFF....WEBP)
    if h.startswith(b"RIFF") and h[8:12] == b"WEBP":
        return "webp"

    # ICO
    if h[:4] == b"\x00\x00\x01\x00":
        return "ico"

    return None


__all__ = ["what"]
