import re
import sys


def run(lines):
    outs = []
    obj = None
    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        if line.startswith("FileLockBoard("):
            obj = FileLockBoard()
            outs.append("null")
        elif line.startswith("lock("):
            m = re.fullmatch(r"lock\((-?\d+),\s*(-?\d+)\)", line)
            outs.append("true" if obj.lock(int(m.group(1)), int(m.group(2))) else "false")
        elif line.startswith("unlock("):
            m = re.fullmatch(r"unlock\((-?\d+),\s*(-?\d+)\)", line)
            outs.append("true" if obj.unlock(int(m.group(1)), int(m.group(2))) else "false")
        elif line.startswith("holder("):
            m = re.fullmatch(r"holder\((-?\d+)\)", line)
            outs.append(str(obj.holder(int(m.group(1)))))
        elif line.startswith("lockedCount("):
            outs.append(str(obj.lockedCount()))
        else:
            raise SystemExit("bad op: " + line)
    return outs


text = sys.stdin.read()
if not text.strip():
    raise SystemExit(0)
print("\n".join(run(text.split("\n"))))
