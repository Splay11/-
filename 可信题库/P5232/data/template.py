import re
import sys


def run(lines):
    outs = []
    obj = None
    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        if line.startswith("MemMgmtSys("):
            m = re.fullmatch(r"MemMgmtSys\((\d+)\)", line)
            obj = MemMgmtSys(int(m.group(1)))
            outs.append("null")
        elif line.startswith("processMemAlloc("):
            m = re.fullmatch(r"processMemAlloc\((-?\d+),\s*(-?\d+)\)", line)
            outs.append(str(obj.processMemAlloc(int(m.group(1)), int(m.group(2)))))
        elif line.startswith("processMemFree("):
            m = re.fullmatch(r"processMemFree\((-?\d+)\)", line)
            obj.processMemFree(int(m.group(1)))
            outs.append("null")
        elif line.startswith("processMemQuery("):
            m = re.fullmatch(r"processMemQuery\((-?\d+)\)", line)
            outs.append(str(obj.processMemQuery(int(m.group(1)))))
        else:
            raise SystemExit("bad op: " + line)
    return outs


text = sys.stdin.read()
if not text.strip():
    raise SystemExit(0)
print("\n".join(run(text.split("\n"))))
