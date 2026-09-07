import os, sys, json, base64, argparse
import ctypes
from ctypes import wintypes

CRYPTPROTECT_UI_FORBIDDEN = 0x01


class DATA_BLOB(ctypes.Structure):
    _fields_ = [("cbData", wintypes.DWORD), ("pbData", ctypes.POINTER(ctypes.c_char))]


def _blob(buf):
    n = len(buf)
    cb = ctypes.create_string_buffer(buf, n)
    return DATA_BLOB(n, ctypes.cast(cb, ctypes.POINTER(ctypes.c_char)))


def unprotect(cipher: bytes) -> bytes:
    out = DATA_BLOB()
    if not ctypes.windll.crypt32.CryptUnprotectData(_blob(cipher), None, None, None, None, CRYPTPROTECT_UI_FORBIDDEN, ctypes.byref(out)):
        raise ctypes.WinError()
    data = ctypes.string_at(out.pbData, out.cbData)
    ctypes.windll.kernel32.LocalFree(out.pbData)
    return data


DEFAULT_VAULT = os.path.expanduser("~/.ucvault_local")


def main():
    ap = argparse.ArgumentParser(description="取回 DPAPI 本地库中的凭据（默认隐藏密值）")
    ap.add_argument("label")
    ap.add_argument("--show", action="store_true", help="显示密值明文")
    ap.add_argument("--vault-dir", default=DEFAULT_VAULT)
    args = ap.parse_args()
    p = os.path.join(os.path.abspath(args.vault_dir), args.label + ".enc")
    if not os.path.exists(p):
        print("NOT_FOUND: " + p)
        sys.exit(2)
    dec = json.loads(unprotect(base64.b64decode(open(p, "rb").read())))
    if "secret_id" in dec:
        print("secret_id:", dec["secret_id"])
        print("secret_key:", dec["secret_key"] if args.show else "<hidden, use --show to reveal>")
    else:
        print("value:", dec["value"] if args.show else "<hidden, use --show to reveal>")


if __name__ == "__main__":
    main()
