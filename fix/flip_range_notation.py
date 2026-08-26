"""按原题记法，把 03 题面里的数据范围改成对侧写法。"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LOG = ROOT / "log"

# 先匹配更长的，避免 10^5 吃掉 10^{18}
SCI_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"\$?\\times\s*10\^\{?18\}?\$?"), "PLACE"),  # handled below
]

# (coeff, exp) → decimal string
def sci_to_dec(coeff: int, exp: int) -> str:
    return str(coeff * 10**exp)


ORIG_COMPACT_RE = re.compile(
    r"10\^\{?-?\d+\}?|\\times\s*10|×\s*10|\d+e\d+|2e\d+|1e\d+",
    re.I,
)
ORIG_EXPANDED_RE = re.compile(r"(?<!\d)(1000000007|1000000000|200000|100000|1000000)(?!\d)")


def original_style(md: str) -> str:
    """返回 compact / expanded / mixed。"""
    # 去掉样例代码块再判断，避免样例数字干扰
    body = re.sub(r"(?:```|~~~).*?(?:```|~~~)", " ", md, flags=re.S)
    compact = bool(ORIG_COMPACT_RE.search(body))
    expanded = bool(ORIG_EXPANDED_RE.search(body))
    if compact and not expanded:
        return "compact"
    if expanded and not compact:
        return "expanded"
    if compact:
        return "compact"
    if expanded:
        return "expanded"
    return "unknown"


SCI_FIND = re.compile(
    r"""
    (?:\$)?
    (?P<coef>\d+)\s*
    (?:\\times|×|\*)\s*
    10\^\{?(?P<exp>\d+)\}?
    (?:\$)?
    |
    (?:\$)?
    10\^\{?(?P<exp2>\d+)\}?
    (?:\$)?
    |
    (?P<ecoef>\d+)[eE](?P<eexp>\d+)
    """,
    re.X,
)


def _sci_repl(m: re.Match[str], use_backtick: bool) -> str:
    if m.group("exp2") is not None:
        coef, exp = 1, int(m.group("exp2"))
    elif m.group("eexp") is not None:
        coef, exp = int(m.group("ecoef")), int(m.group("eexp"))
    else:
        coef, exp = int(m.group("coef")), int(m.group("exp"))
    if exp < 3:
        return m.group(0)
    dec = sci_to_dec(coef, exp)
    return f"`{dec}`" if use_backtick else dec


def expand_sci(text: str) -> str:
    text = re.sub(r"\$10\^9\+7\$", "`1000000007`", text)
    text = re.sub(r"10\^\{9\}\+7", "1000000007", text)
    text = re.sub(r"10\^9\+7", "1000000007", text)
    parts = text.split("$")
    out = []
    for i, part in enumerate(parts):
        in_math = i % 2 == 1
        out.append(SCI_FIND.sub(lambda m: _sci_repl(m, use_backtick=not in_math), part))
    joined = "$".join(out)
    joined = re.sub(r"\$(\d{4,})\$", r"`\1`", joined)
    return joined


# 展开 → 科学计数（长的优先）
DEC_TO_SCI = [
    (re.compile(r"`?1000000007`?"), r"$10^9+7$"),
    (re.compile(r"`?1000000000000000000`?"), r"$10^{18}$"),
    (re.compile(r"`?1000000000`?"), r"$10^9$"),
    (re.compile(r"`?2000000000`?"), r"$2 \\times 10^9$"),
    (re.compile(r"`?500000`?"), r"$5 \\times 10^5$"),
    (re.compile(r"`?400000`?"), r"$4 \\times 10^5$"),
    (re.compile(r"`?300000`?"), r"$3 \\times 10^5$"),
    (re.compile(r"`?200000`?"), r"$2 \\times 10^5$"),
    (re.compile(r"`?100000`?"), r"$10^5$"),
    (re.compile(r"`?1000000`?"), r"$10^6$"),
    (re.compile(r"`?10000`?"), r"$10^4$"),
]


def collapse_dec(text: str) -> str:
    for pat, rep in DEC_TO_SCI:
        text = pat.sub(rep, text)
    return text


def convert_fields(obj: dict, style: str) -> dict:
    fn = expand_sci if style == "compact" else collapse_dec if style == "expanded" else (lambda x: x)
    out = dict(obj)
    for k in ("content", "input_description", "output_description"):
        if k in out and isinstance(out[k], str):
            out[k] = fn(out[k])
    return out


def process(pid: str) -> str:
    d = LOG / pid
    orig = (d / "01_原始题面.md").read_text(encoding="utf-8")
    p03 = d / "03_LLM生成的新题面.json"
    obj = json.loads(p03.read_text(encoding="utf-8"))
    style = original_style(orig)
    new = convert_fields(obj, style)
    if new == obj:
        return f"{pid} {style} unchanged"
    p03.write_text(json.dumps(new, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return f"{pid} {style} flipped"


def main() -> None:
    pids = [l.strip() for l in (ROOT / "all.txt").read_text(encoding="utf-8-sig").splitlines() if l.strip()]
    n = 0
    for pid in pids:
        msg = process(pid)
        if "flipped" in msg:
            n += 1
            print(msg)
    print("flipped", n, "of", len(pids))


if __name__ == "__main__":
    main()
