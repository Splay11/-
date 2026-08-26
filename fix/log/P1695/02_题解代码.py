import re, sys
s = sys.stdin.read().strip()
inner = s[1:-1] if s.startswith("[") else s
parts = [p.strip() for p in inner.split(",") if p.strip()]
vals, cnts = [], []
for p in parts:
    m = re.fullmatch(r"(-?\d+)\((\d+)\)", p)
    if not m:
        m = re.fullmatch(r"(-?\d+)", p)
        v, c = int(m.group(1)), 1
    else:
        v, c = int(m.group(1)), int(m.group(2))
    if vals and vals[-1] == v:
        cnts[-1] += c
    else:
        vals.append(v); cnts.append(c)
print("[" + ",".join(f"{v}({c})" for v, c in zip(vals, cnts)) + "]")
