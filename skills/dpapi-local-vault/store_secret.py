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



def run_selftest():
    """自检：临时保险库目录内跑真实 main() 存储流程——双行输入（id/key）落盘 +
    meta 标注 + 回环校验须 STORED_OK（须过）；空输入须 MISSING_INPUT rc=2（须拦）；
    --exposed 须标 EXPOSED_PENDING_ROTATION。
    平台说明：DPAPI 加解密是 Windows 原语（ctypes.windll），本机非 Windows 无法实跑；
    非 Windows 时仅在自检内以可逆测试封套替身 protect/unprotect，stdin 解析、落盘
    信封、meta 标注、回环校验等其余逻辑均为真实代码；Windows 上则直接实跑真实
    DPAPI 回环。未实跑部分：DPAPI 原语本身（非 Windows 时）。"""
    import contextlib, io, tempfile
    passed = failed = 0

    def check(name, cond):
        nonlocal passed, failed
        if cond:
            passed += 1
        else:
            failed += 1
            print("  [FAIL] " + name)

    check("DATA_BLOB 封送长度正确", _blob(b"abc").cbData == 3)
    on_windows = sys.platform.startswith("win")
    real_protect, real_unprotect = protect, unprotect
    if not on_windows:
        def fake_protect(plain):
            return base64.b64encode(plain[::-1])

        def fake_unprotect(cipher):
            return base64.b64decode(cipher)[::-1]

        globals()["protect"] = fake_protect
        globals()["unprotect"] = fake_unprotect
    try:
        def call(argv, stdin_text):
            old_argv, old_stdin = sys.argv, sys.stdin
            sys.argv = ["store_secret.py"] + argv
            sys.stdin = io.StringIO(stdin_text)
            buf = io.StringIO()
            code = 0
            try:
                with contextlib.redirect_stdout(buf):
                    main()
            except SystemExit as e:
                code = e.code if isinstance(e.code, int) else 1
            finally:
                sys.argv, sys.stdin = old_argv, old_stdin
            return code, buf.getvalue()

        with tempfile.TemporaryDirectory() as td:
            code, out = call(["tok1", "--vault-dir", td], "myid\nmykey\n")
            enc = os.path.join(td, "tok1.enc")
            with open(os.path.join(td, "tok1.meta.json"), encoding="utf-8") as f:
                meta = json.load(f)
            check("双行凭据存储 STORED_OK 且落盘",
                  code == 0 and "STORED_OK" in out and os.path.isfile(enc))
            check("meta 标注 status=OK/exposed=False",
                  meta["status"] == "OK" and meta["exposed"] is False
                  and meta["label"] == "tok1")
            code, out = call(["tok2", "--vault-dir", td, "--exposed",
                              "--exposed-where", "chat"], "onlyvalue")
            with open(os.path.join(td, "tok2.meta.json"), encoding="utf-8") as f:
                meta2 = json.load(f)
            check("单行值 + --exposed → EXPOSED_PENDING_ROTATION",
                  code == 0 and "STORED_OK" in out
                  and meta2["status"] == "EXPOSED_PENDING_ROTATION")
            code, out = call(["tok3", "--vault-dir", td], "")
            check("空输入 MISSING_INPUT rc=2", code == 2 and "MISSING_INPUT" in out)
    finally:
        globals()["protect"] = real_protect
        globals()["unprotect"] = real_unprotect
    if not on_windows:
        print("  [NOTE] 非 Windows：DPAPI 原语未实跑（测试封套替代）；"
              "存储/解析/meta/回环逻辑已实跑")
    print(f"SELFTEST: {passed} passed, {failed} failed — {'PASS' if failed == 0 else 'FAIL'}")
    return 0 if failed == 0 else 1

def main():
    if "--selftest" in sys.argv[1:]:
        sys.exit(run_selftest())
    ap = argparse.ArgumentParser(description="用 Windows DPAPI 把凭据加密存到本机（免口令，仅当前用户可解）")
    ap.add_argument("--selftest", action="store_true", help="自检（临时夹具，不触碰真实文件）")
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
