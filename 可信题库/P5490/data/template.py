import re
import sys


def run(lines):
    outs = []
    obj = None
    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        m = re.fullmatch(r"ParcelSlots\((-?\d+)\)", line)
        if m:
            obj = ParcelSlots(int(m.group(1)))
            outs.append("null")
        elif line.startswith("put("):
            m = re.fullmatch(r"put\((-?\d+),\s*(-?\d+)\)", line)
            if not m:
                raise SystemExit("bad op: " + line)
            outs.append("true" if obj.put(int(m.group(1)), int(m.group(2))) else "false")
        elif line.startswith("take("):
            m = re.fullmatch(r"take\((-?\d+)\)", line)
            if not m:
                raise SystemExit("bad op: " + line)
            outs.append(str(obj.take(int(m.group(1)))))
        elif line.startswith("moveRight("):
            m = re.fullmatch(r"moveRight\((-?\d+)\)", line)
            if not m:
                raise SystemExit("bad op: " + line)
            outs.append("true" if obj.moveRight(int(m.group(1))) else "false")
        elif line == "occupied()":
            outs.append(str(obj.occupied()))
        else:
            raise SystemExit("bad op: " + line)
    return outs


text = sys.stdin.read()
if not text.strip():
    raise SystemExit(0)
print("\n".join(run(text.split("\n"))))
