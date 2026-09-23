# -*- coding: utf-8 -*-
import os, re, subprocess, sys, time
from pathlib import Path
from html import unescape
import requests

ROOT = Path(r"d:\机考出题\problem-maker")
PROBS = ROOT / "Problems"
UTILS = ROOT / "utils"
TMP = PROBS / "_beginner_submit_tmp"
TMP.mkdir(exist_ok=True)
BASE = "https://codefun2000.com"
PIDS = ["P7012", "P7013", "P7014"]

os.environ["HYDRO_API_UNAME"] = os.environ.get("HYDRO_API_UNAME") or "luti"
os.environ["HYDRO_API_PASSWORD"] = os.environ.get("HYDRO_API_PASSWORD") or "lutilutiluti1014lutilutiluti"
py = sys.executable


def run(cmd):
    print("+", " ".join(cmd), flush=True)
    p = subprocess.run(cmd, cwd=str(ROOT))
    if p.returncode != 0:
        raise SystemExit(p.returncode)


def extract(sol: Path, heading: str, fence: str) -> str:
    text = sol.read_text(encoding="utf-8")
    parts = re.split(r"(?m)^###\s+", text)
    for part in parts:
        first = part.splitlines()[0].strip() if part.strip() else ""
        if first == heading or (heading == "C" and re.fullmatch(r"C\s*", first)):
            m = re.search(rf"```{fence}\s*\n(.*?)```", part, re.S)
            if m:
                return m.group(1)
    raise ValueError(f"no {heading} in {sol}")


def parse_form(html: str) -> dict:
    fields = {}
    for m in re.finditer(r"<(input|textarea)\b([^>]*)>", html, re.I):
        tag, attrs = m.group(1).lower(), m.group(2)
        nm = re.search(r'name="([^"]+)"', attrs)
        if not nm:
            continue
        name = unescape(nm.group(1))
        if tag == "input":
            typ = (re.search(r'type="([^"]+)"', attrs, re.I) or [None, "text"])[1].lower()
            if typ in ("submit", "button", "file", "image"):
                continue
            vm = re.search(r'value="([^"]*)"', attrs)
            fields[name] = unescape(vm.group(1)) if vm else ""
    for m in re.finditer(r"<textarea\b([^>]*)>(.*?)</textarea>", html, re.I | re.S):
        attrs, body = m.group(1), m.group(2)
        nm = re.search(r'name="([^"]+)"', attrs)
        if nm:
            fields[unescape(nm.group(1))] = unescape(body)
    return fields


def parse_title(pid: str):
    title = tag = diff = ""
    for line in (PROBS / pid / "标题.txt").read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("标题"):
            title = line.split("：", 1)[-1].split(":", 1)[-1].strip()
        elif "标签" in line:
            tag = line.split("：", 1)[-1].split(":", 1)[-1].strip()
        elif line.startswith("难度"):
            diff = line.split("：", 1)[-1].split(":", 1)[-1].strip()
    return title, tag, diff


def submit(pid, lang, code):
    cmd = [
        py, str(UTILS / "submit_code_and_get_result.py"),
        "--base-url", BASE, "--domain-id", "system", "--pid", pid,
        "--lang", lang, "--code-file", str(code),
    ]
    env = os.environ.copy(); env["PYTHONIOENCODING"] = "utf-8"
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", env=env)
    out = (p.stdout or "") + "\n" + (p.stderr or "")
    (TMP / f"{pid}_{lang.replace('.','_')}.txt").write_text(out, encoding="utf-8")
    if '"isAccepted": true' in out or '"isAccepted":true' in out:
        return "Accepted"
    for n in ("Wrong Answer", "Runtime Error", "Compile Error", "Time Limit Exceeded"):
        if f'"name": "{n}"' in out:
            return n
    if "403" in out:
        return "LOGIN_FAIL"
    return "UNKNOWN"


for pid in PIDS:
    run([py, str(UTILS / "upload_problem.py"), "--base-url", BASE, "--domain-id", "system", "--pid", pid,
         "--statement", str(PROBS / pid / "题面.md"), "--solution", str(PROBS / pid / "题解.md")])
    run([py, str(UTILS / "upload_testdata.py"), "--base-url", BASE, "--domain-id", "system", "--pid", pid,
         "--data-dir", str(PROBS / pid / "data")])

s = requests.Session(); s.trust_env = False
s.post(f"{BASE}/login", data={"uname": os.environ["HYDRO_API_UNAME"], "password": os.environ["HYDRO_API_PASSWORD"]}, timeout=30)
for pid in PIDS:
    title, tag, diff = parse_title(pid)
    html = s.get(f"{BASE}/p/{pid}/edit", timeout=30).text
    fields = parse_form(html)
    fields["title"] = title
    if "alg_tag" in fields:
        fields["alg_tag"] = tag
    if "difficulty" in fields:
        fields["difficulty"] = diff
    if "content" in fields:
        fields["content"] = (PROBS / pid / "题面.md").read_text(encoding="utf-8").strip()
    r = s.post(f"{BASE}/p/{pid}/edit", data=fields, timeout=60)
    print(pid, "edit", r.status_code, title, tag, diff, flush=True)

langs = [("py.py3", "Python", "python", ".py"), ("java", "Java", "java", ".java"),
         ("cc.cc14o2", "C++", "cpp", ".cc"), ("c", "C", "c", ".c")]
rows = []
for pid in PIDS:
    sol = PROBS / pid / "题解.md"
    for lang, heading, fence, ext in langs:
        code = TMP / f"{pid}{ext}"
        body = extract(sol, heading, fence)
        if lang == "java" and "public class Solution" not in body and "class Solution" in body:
            body = body.rstrip() + "\n"
        code.write_text(body, encoding="utf-8")
        print(f"{pid} {lang} ...", flush=True)
        st = submit(pid, lang, code)
        if st in ("LOGIN_FAIL", "UNKNOWN"):
            time.sleep(15)
            st = submit(pid, lang, code)
        print(" ->", st, flush=True)
        rows.append(f"{pid} {lang} {st}")
        time.sleep(3)
(TMP / "result.txt").write_text("\n".join(rows) + "\n", encoding="utf-8")
print("\n".join(rows))
