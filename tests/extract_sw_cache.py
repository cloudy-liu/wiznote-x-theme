"""Extract WizNote Service Worker cache entries (Chromium simple cache format).

Usage: python tests/extract_sw_cache.py <cache_dir> <out_dir>

Each <hash>_0 file: SimpleFileHeader + key(URL) + stream1(body) + EOF1 + stream0(headers) + [sha256] + EOF0.
Structs are 8-byte aligned: header and EOF records are 24 bytes each (<QLLL + 4 pad).
"""
import gzip
import io
import os
import re
import struct
import sys
import zlib

INITIAL_MAGIC = 0xFCFB6D1BA7725C30
FINAL_MAGIC = 0xF4FA6F45970D41D8
FLAG_HAS_KEY_SHA256 = 2

try:
    import brotli  # type: ignore
except ImportError:
    brotli = None


def parse_entry(path):
    data = open(path, "rb").read()
    if len(data) < 40:
        return None
    magic, version, key_len, _key_hash = struct.unpack_from("<QLLL", data, 0)
    if magic != INITIAL_MAGIC:
        return None
    key = data[24:24 + key_len].decode("utf-8", "replace")
    # EOF0 record is the last 24 bytes (20 + 4 pad)
    magic0, flags0, _crc0, stream0_size = struct.unpack_from("<QLLL", data, len(data) - 24)
    if magic0 != FINAL_MAGIC:
        return None
    sha_len = 32 if (flags0 & FLAG_HAS_KEY_SHA256) else 0
    stream0_start = len(data) - 24 - sha_len - stream0_size
    stream0 = data[stream0_start:stream0_start + stream0_size]
    # EOF1 record sits just before stream0
    eof1_at = stream0_start - 24
    body = b""
    if eof1_at >= 24 + key_len:
        magic1, _f1, _c1, stream1_size = struct.unpack_from("<QLLL", data, eof1_at)
        if magic1 == FINAL_MAGIC:
            body_start = 24 + key_len
            body = data[body_start:body_start + stream1_size]
    return key, body, stream0


def decompress(body):
    if body[:2] == b"\x1f\x8b":
        try:
            return gzip.GzipFile(fileobj=io.BytesIO(body)).read()
        except Exception:
            pass
    # try raw deflate / zlib
    for wbits in (zlib.MAX_WBITS, -zlib.MAX_WBITS):
        try:
            return zlib.decompress(body, wbits)
        except Exception:
            pass
    if brotli is not None:
        try:
            return brotli.decompress(body)
        except Exception:
            pass
    return body


def safe_name(url):
    name = re.sub(r"^https?://", "", url)
    name = re.sub(r"[^A-Za-z0-9._-]", "_", name)
    return name[-150:]


def main():
    cache_dir, out_dir = sys.argv[1], sys.argv[2]
    os.makedirs(out_dir, exist_ok=True)
    index = []
    for root, _dirs, files in os.walk(cache_dir):
        for fn in files:
            if not fn.endswith("_0"):
                continue
            path = os.path.join(root, fn)
            try:
                parsed = parse_entry(path)
            except Exception:
                parsed = None
            if not parsed:
                continue
            key, body, stream0 = parsed
            body = decompress(body)
            out_path = os.path.join(out_dir, safe_name(key))
            with open(out_path, "wb") as f:
                f.write(body)
            ctype = ""
            m = re.search(rb"content-type\x00([^\x00]+)", stream0, re.I)
            if m:
                ctype = m.group(1).decode("ascii", "replace")
            index.append((key, len(body), ctype, os.path.basename(out_path)))
    index.sort()
    with open(os.path.join(out_dir, "_index.tsv"), "w", encoding="utf-8") as f:
        for key, size, ctype, name in index:
            f.write(f"{key}\t{size}\t{ctype}\t{name}\n")
    print(f"extracted {len(index)} entries -> {out_dir}")


if __name__ == "__main__":
    main()
