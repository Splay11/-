"""原题样例禁区：新样例不得等于原样例，也不得复用原样例中的特征行。"""
from __future__ import annotations

import re

_FENCE = r"(?:```|~~~)[^\n]*\n(.*?)(?:```|~~~)"


def _norm_ws(s: str) -> str:
    s = (s or "").replace("\r\n", "\n").strip()
    s = re.sub(r"[ \t]+", " ", s)
    return s


def extract_original_sample_inputs(md: str) -> list[str]:
    pats = [
        rf"\*\*[^\n]*输入[^\n]*\*\*\s*\n\s*{_FENCE}",
        rf"#{1,3}\s*输入(?!描述)[^\n]*\n+{_FENCE}",
        rf"样例输入[^\n]*\n+{_FENCE}",
        rf"输入[：:]?\s*\n+{_FENCE}",
        r"```input\d*\n(.*?)```",
    ]
    found: list[str] = []
    for p in pats:
        found += [_norm_ws(x) for x in re.findall(p, md, re.S)]
    out: list[str] = []
    for x in found:
        if x and x not in out:
            out.append(x)
    return out


def _signature_lines(sample_input: str) -> list[str]:
    """原样例里足够有辨识度的行：含字母/问号，或至少 3 个数字。"""
    sigs: list[str] = []
    for raw in sample_input.splitlines():
        line = raw.strip()
        if not line:
            continue
        if re.search(r"[A-Za-z?]", line):
            sigs.append(line)
            continue
        nums = re.findall(r"-?\d+", line)
        if len(nums) >= 3:
            sigs.append(line)
    return sigs


def original_forbidden(md: str) -> dict:
    inputs = extract_original_sample_inputs(md)
    lines: list[str] = []
    for inp in inputs:
        for line in _signature_lines(inp):
            if line not in lines:
                lines.append(line)
    return {"inputs": inputs, "lines": lines}


def sample_hits_original(new_input: str, forbidden: dict) -> str | None:
    """若新样例撞原样例，返回原因，否则 None。"""
    n = _norm_ws(new_input)
    n_space = re.sub(r"\s+", " ", n)
    if not n:
        return "empty"
    for orig in forbidden.get("inputs") or []:
        o = re.sub(r"\s+", " ", orig)
        if n_space == o:
            return "exact"
        tokens = o.split()
        if (len(o) >= 12 or len(tokens) >= 4) and (o in n_space or n_space in o):
            return "substring"
    new_lines = [ln.strip() for ln in new_input.replace("\r\n", "\n").splitlines() if ln.strip()]
    new_line_set = set(new_lines)
    for line in forbidden.get("lines") or []:
        if line in new_line_set:
            return f"line:{line}"
        if re.search(r"[A-Za-z?]", line) and len(line) >= 2:
            for nl in new_lines:
                if line in nl:
                    return f"substr:{line}"
    return None
