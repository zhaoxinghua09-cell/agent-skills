import os, sys, json, base64, argparse, subprocess, datetime
import ctypes
from ctypes import wintypes

CRYPTPROTECT_UI_FORBIDDEN = 0x01


class DATA_BLOB(ctypes.Structure):
    _fields_ = [("cbData", wintypes.DWORD), ("pbData", ctypes.POINTER(ctypes.c_char))]


def _blob(buf):
    n = len(buf)
    cb = ctypes.create_string_buffer(buf, n)
    return DATA_BLOB(n, ctypes.cast(cb, ctypes.POINTER(ctypes.c_char)))


def protect(plain: bytes) -> bytes:
    out = DATA_BLOB()
    if not ctypes.windll.crypt32.CryptProtectData(_blob(plain), None, None, None, None, CRYPTPROTECT_UI_FORBIDDEN, ctypes.byref(out)):
        raise ctypes.WinError()
    data = ctypes.string_at(out.pbData, out.cbData)
    ctypes.windll.kernel32.LocalFree(out.pbData)
    return data


def unprotect(cipher: bytes) -> bytes:
    out = DATA_BLOB()
    if not ctypes.windll.crypt32.CryptUnprotectData(_blob(cipher), None, None, None, None, CRYPTPROTECT_UI_FORBIDDEN, ctypes.byref(out)):
        raise ctypes.WinError()
    data = ctypes.string_at(out.pbData, out.cbData)
    ctypes.windll.kernel32.LocalFree(out.pbData)
    return data


DEFAULT_VAULT = os.path.expanduser("~/.ucvault_local")


def main():
    ap = argparse.ArgumentParser(description="用 Windows DPAPI 把凭据加密存到本机（免口令，仅当前用户可解）")
    ap.add_argument("label", help="凭据标签，如 tencent_cos")
    ap.add_argument("--scope", default="secret", help="密级/作用域说明")
    ap.add_argument("--notes", default="", help="备注（用途/作用域）")
    ap.add_argument("--vault-dir", default=DEFAULT_VAULT, help="保险库目录")
    ap.add_argument("--exposed", action="store_true", help="标注此凭据已在不安全渠道（如聊天）明文暴露")
    ap.add_argument("--exposed-where", default="", help="暴露位置")
    ap.add_argument("--exposed-at", default="", help="暴露时间")
    args = ap.parse_args()

    raw = sys.stdin.read()
    lines = [l.rstrip("\r") for l in raw.split("\n")]
    lines = [l for l in lines if l != ""]
    if not lines:
        print("MISSING_INPUT")
        sys.exit(2)
    if len(lines) == 2:
        payload = {"secret_id": lines[0], "secret_key": lines[1]}
    else:
        payload = {"value": "\n".join(lines)}

    enc = protect(json.dumps(payload, ensure_ascii=False).encode("utf-8"))
    d = os.path.abspath(args.vault_dir)
    os.makedirs(d, exist_ok=True)
    p = os.path.join(d, args.label + ".enc")
    with open(p, "wb") as f:
        f.write(base64.b64encode(enc))
    # 锁权限：去掉继承，只给当前用户完全控制
    user = os.environ.get("USERNAME", "")
    if user:
        try:
            subprocess.run(["icacls", p, "/inheritance:r", "/grant:r", f"{user}:F"],
                            capture_output=True, text=True, errors="ignore", check=False)
        except Exception:
            pass
    try:
        os.chmod(p, 0o600)
    except Exception:
        pass

    # 泄漏标注 meta
    exposed = bool(args.exposed)
    meta = {
        "label": args.label,
        "scope": args.scope,
        "notes": args.notes,
        "store_ref": "vault://local/ucvault_local/" + args.label + ".enc",
        "enc_method": "Windows DPAPI (CryptProtectData) + base64；仅当前用户可解，换机/换账号不可解",
        "exposed": exposed,
        "exposed_where": args.exposed_where or ("unknown" if exposed else ""),
        "exposed_at": args.exposed_at or ("unknown" if exposed else ""),
        "status": "EXPOSED_PENDING_ROTATION" if exposed else "OK",
        "annotated_at": datetime.date.today().isoformat(),
        "annotated_by": "dpapi-local-vault",
    }
    with open(os.path.join(d, args.label + ".meta.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    # 回环校验（解密后比对，绝不打印明文）
    dec = json.loads(unprotect(base64.b64decode(open(p, "rb").read())))
    ok = (dec.get("secret_id") == payload.get("secret_id")
          and dec.get("secret_key") == payload.get("secret_key")
          and dec.get("value") == payload.get("value"))
    print("STORED_OK" if ok else "VERIFY_FAIL")


if __name__ == "__main__":
    main()
