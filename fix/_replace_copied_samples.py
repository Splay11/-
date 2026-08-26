"""去掉与原题相同或复用原特征行的样例，不足 2 条时用标程再造新输入。"""
from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

from forbid_orig_sample import original_forbidden, sample_hits_original

ROOT = Path(__file__).resolve().parent
LOG = ROOT / "log"


def py_from_35(md: str) -> str | None:
    m = re.search(r"### Python\s+```(?:python)?\s*\n(.*?)```", md, re.S)
    if m and len(m.group(1).strip()) > 8:
        return m.group(1).strip()
    return None


def run_code(code: str, stdin_text: str, timeout: int = 8) -> str:
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, encoding="utf-8") as f:
        f.write(code)
        path = f.name
    try:
        r = subprocess.run(
            [sys.executable, path],
            input=stdin_text if stdin_text.endswith("\n") else stdin_text + "\n",
            capture_output=True,
            text=True,
            timeout=timeout,
            encoding="utf-8",
        )
    finally:
        Path(path).unlink(missing_ok=True)
    if r.returncode != 0:
        raise RuntimeError((r.stderr or "")[-400:] or f"exit {r.returncode}")
    return r.stdout.replace("\r\n", "\n").rstrip("\n")


def mutate_token(tok: str, k: int) -> str:
    if re.fullmatch(r"[dp?]+", tok):
        t = tok.translate(str.maketrans("dp", "pd"))
        if k == 0:
            return t
        chars = list(t if k % 2 else tok)
        for i in range(len(chars)):
            if chars[i] == "?":
                chars[i] = "d" if (i + k) % 2 == 0 else "p"
            elif k >= 2:
                chars[i] = "p" if chars[i] == "d" else "d"
        s = "".join(chars)
        if s != tok:
            return s
        return tok[::-1] if tok[::-1] != tok else ("p" * len(tok) if tok != "p" * len(tok) else "d" * len(tok))
    if re.fullmatch(r"[A-Za-z?]+", tok) and len(tok) >= 2:
        rot = tok[k % len(tok) :] + tok[: k % len(tok)]
        if rot != tok:
            return rot
        return tok[::-1]
    if re.fullmatch(r"-?\d+", tok):
        return str(int(tok) + (1 if k % 2 == 0 else -1) * ((k // 2) + 1))
    return tok


def bump_line(line: str, delta: int) -> str:
    parts = line.split()
    out = []
    for tok in parts:
        if re.fullmatch(r"-?\d+", tok):
            val = int(tok) + delta
            if int(tok) >= 1 and val < 1:
                return None
            out.append(str(val))
        else:
            out.append(mutate_token(tok, abs(delta)))
    return " ".join(out) if out else line


def rewrite_string_tree(inp: str, k: int) -> str | None:
    """n + 长度为 n 的 d/p/? 串 + n-1 条边 → 换成新串 + 路径树。"""
    lines = inp.replace("\r\n", "\n").strip().split("\n")
    if len(lines) < 3:
        return None
    first = lines[0].split()
    if len(first) != 1 or not re.fullmatch(r"\d+", first[0]):
        return None
    n = int(first[0])
    s = lines[1].strip()
    if not re.fullmatch(r"[dp?]+", s) or len(s) != n:
        return None
    if len(lines) != n + 1:
        return None
    news = mutate_token(s, k)
    if news == s:
        news = mutate_token(s, k + 3)
    if len(news) != n:
        news = (news + "d" * n)[:n]
    if k % 2 == 0:
        edges = [f"{i} {i + 1}" for i in range(1, n)]
    else:
        edges = [f"1 {i}" for i in range(2, n + 1)]
    return f"{n}\n{news}\n" + "\n".join(edges)


def variants(inp: str) -> list[str]:
    lines = inp.replace("\r\n", "\n").strip().split("\n")
    cands: list[str] = []
    if not lines:
        return cands
    for k in range(6):
        t = rewrite_string_tree(inp, k)
        if t:
            cands.append(t)
    for d in (1, 2, 3, -1):
        ls = lines[:]
        last = bump_line(ls[-1], d)
        if last is not None:
            ls[-1] = last
            cands.append("\n".join(ls))
        if len(lines) >= 2:
            ls2 = lines[:]
            mid = bump_line(ls2[-2], d)
            if mid is not None:
                ls2[-2] = mid
                cands.append("\n".join(ls2))
            ls3 = lines[:]
            sec = bump_line(ls3[1], d)
            if sec is not None:
                ls3[1] = sec
                cands.append("\n".join(ls3))
    first = lines[0].split()
    if first and all(re.fullmatch(r"-?\d+", x) for x in first) and len(first) == 1:
        n = int(first[0])
        if 1 <= n <= 20:
            ls = lines[:]
            ls[0] = str(n + 1 if n < 10 else max(1, n - 1))
            cands.append("\n".join(ls))
    seen = set()
    out = []
    base = inp.replace("\r\n", "\n").strip()
    for c in cands:
        c = c.strip()
        if c and c != base and c not in seen:
            seen.add(c)
            out.append(c)
    return out


def handmade_tree_dp(n: int, s: str, star: bool) -> str:
    if star:
        edges = [f"1 {i}" for i in range(2, n + 1)]
    else:
        edges = [f"{i} {i + 1}" for i in range(1, n)]
    return f"{n}\n{s}\n" + "\n".join(edges)


def extra_seeds(pid: str, forbidden: dict) -> list[str]:
    """部分题型用固定全新输入，避免变异仍带原特征串。"""
    if pid == "P3359":
        return [
            handmade_tree_dp(2, "pp", False),
            handmade_tree_dp(3, "dpd", False),
            handmade_tree_dp(4, "????", False),
            handmade_tree_dp(4, "pd?d", True),
            handmade_tree_dp(6, "p?d?p?", False),
        ]
    return []


def process(pid: str) -> str:
    d = LOG / pid
    orig_md = (d / "01_原始题面.md").read_text(encoding="utf-8")
    forbidden = original_forbidden(orig_md)
    samples = json.loads((d / "04_LLM生成的新样例.json").read_text(encoding="utf-8"))["samples"]
    kept = [s for s in samples if not sample_hits_original(s.get("input", ""), forbidden)]
    if pid == "P3359":
        kept = [s for s in kept if not re.search(r"(^|\s)0(\s|$)", s.get("input", ""))]
    dropped = len(samples) - len(kept)
    if dropped == 0 and len(kept) >= 2:
        return "ok"

    py = py_from_35((d / "03.5_修改后的题解.md").read_text(encoding="utf-8"))
    seeds = extra_seeds(pid, forbidden)
    seeds += [s["input"] for s in kept] + [s["input"] for s in samples]
    seeds += list(forbidden.get("inputs") or [])

    used_norm = {re.sub(r"\s+", " ", (s.get("input") or "").strip()) for s in kept}

    def try_add(cand: str) -> bool:
        nonlocal kept
        if sample_hits_original(cand, forbidden):
            return False
        if pid == "P3359" and re.search(r"(^|\s)0(\s|$)", cand):
            return False
        key = re.sub(r"\s+", " ", cand.strip())
        if key in used_norm:
            return False
        if not py:
            return False
        try:
            out = run_code(py, cand)
        except Exception:
            return False
        kept.append({"input": cand, "output": out, "explanation": "按题意模拟计算得到。"})
        used_norm.add(key)
        return True

    for seed in seeds:
        if len(kept) >= 3:
            break
        try_add(seed)
        if len(kept) >= 3:
            break
        for cand in variants(seed):
            if try_add(cand) and len(kept) >= 3:
                break

    if len(kept) < 2:
        return f"FAIL remain={len(kept)} dropped={dropped} py={bool(py)}"

    (d / "04_LLM生成的新样例.json").write_text(
        json.dumps({"samples": kept[:4]}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return f"rewrote dropped={dropped} now={min(len(kept), 4)}"


def main() -> None:
    pids = [l.strip() for l in (ROOT / "all.txt").read_text(encoding="utf-8-sig").splitlines() if l.strip()]
    fail = []
    changed = []
    ok = []
    for pid in pids:
        msg = process(pid)
        print(pid, msg)
        if msg.startswith("FAIL"):
            fail.append(pid)
        elif msg.startswith("rewrote"):
            changed.append(pid)
        else:
            ok.append(pid)
    print("ok", len(ok), "changed", len(changed), "fail", fail)


if __name__ == "__main__":
    main()
