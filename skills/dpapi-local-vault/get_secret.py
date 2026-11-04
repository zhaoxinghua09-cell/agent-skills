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



def run_selftest():
    """自检：临时保险库内跑真实 main() 取回流程——默认隐藏密值且不泄漏（须过）；
    --show/--raw 输出与写入值一致，未知标签须 NOT_FOUND rc=2（须拦）。
    平台说明：DPAPI 解密是 Windows 原语（ctypes.windll），本机非 Windows 无法实跑；
    Windows 上借同目录 store_secret.protect 造真实 DPAPI 密文夹具实跑；非 Windows
    时仅在自检内以可逆测试封套替身 unprotect，信封解码、隐藏/裸输出、缺失处理等
    其余逻辑均为真实代码。未实跑部分：DPAPI 原语本身（非 Windows 时）。"""
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
    real_unprotect = unprotect
    payload = {"secret_id": "myid", "secret_key": "mykey"}
    plain = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    if on_windows:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import store_secret
        cipher = store_secret.protect(plain)
    else:
        def fake_unprotect(c):
            return base64.b64decode(c)[::-1]

        globals()["unprotect"] = fake_unprotect
        cipher = base64.b64encode(plain[::-1])
    try:
        def call(argv):
            old = sys.argv
            sys.argv = ["get_secret.py"] + argv
            buf = io.StringIO()
            code = 0
            try:
                with contextlib.redirect_stdout(buf):
                    main()
            except SystemExit as e:
                code = e.code if isinstance(e.code, int) else 1
            finally:
                sys.argv = old
            return code, buf.getvalue()

        with tempfile.TemporaryDirectory() as td:
            p = os.path.join(td, "tok.enc")
            with open(p, "wb") as f:
                f.write(base64.b64encode(cipher))
            code, out = call(["tok", "--vault-dir", td])
            check("默认隐藏密值且不泄漏 key",
                  code == 0 and "secret_id: myid" in out and "mykey" not in out
                  and "<hidden" in out)
            code, out = call(["tok", "--vault-dir", td, "--show"])
            check("--show 显示密值", code == 0 and "secret_key: mykey" in out)
            code, out = call(["tok", "--vault-dir", td, "--raw"])
            check("--raw 输出 id<TAB>key", code == 0 and out.strip() == "myid\tmykey")
            code, out = call(["nope", "--vault-dir", td])
            check("未知标签 NOT_FOUND rc=2", code == 2 and "NOT_FOUND" in out)
    finally:
        globals()["unprotect"] = real_unprotect
    if not on_windows:
        print("  [NOTE] 非 Windows：DPAPI 原语未实跑（测试封套替代）；"
              "信封/隐藏/裸输出逻辑已实跑")
    print(f"SELFTEST: {passed} passed, {failed} failed — {'PASS' if failed == 0 else 'FAIL'}")
    return 0 if failed == 0 else 1

def main():
    if "--selftest" in sys.argv[1:]:
        sys.exit(run_selftest())
    ap = argparse.ArgumentParser(description="取回 DPAPI 本地库中的凭据（默认隐藏密值）")
    ap.add_argument("--selftest", action="store_true", help="自检（临时夹具，不触碰真实文件）")
    ap.add_argument("label")
    ap.add_argument("--show", action="store_true", help="显示密值明文")
    ap.add_argument("--raw", action="store_true",
                    help="只输出裸值（value 条目单行输出；secret_id 条目输出 'id<TAB>key'），无标签前缀——供脚本直接消费，勿打印到聊天/日志")
    ap.add_argument("--vault-dir", default=DEFAULT_VAULT)
    args = ap.parse_args()
    p = os.path.join(os.path.abspath(args.vault_dir), args.label + ".enc")
    if not os.path.exists(p):
        print("NOT_FOUND: " + p)
        sys.exit(2)
    dec = json.loads(unprotect(base64.b64decode(open(p, "rb").read())))
    if args.raw:
        if "secret_id" in dec:
            print(dec["secret_id"] + "\t" + dec.get("secret_key", ""))
        else:
            print(dec.get("value", ""))
        return
    if "secret_id" in dec:
        print("secret_id:", dec["secret_id"])
        print("secret_key:", dec["secret_key"] if args.show else "<hidden, use --show to reveal>")
    else:
        print("value:", dec["value"] if args.show else "<hidden, use --show to reveal>")


if __name__ == "__main__":
    main()
