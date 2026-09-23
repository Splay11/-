import re
import sys


def run(lines):
    outs = []
    obj = None
    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        if line.startswith("TTLCache("):
            m = re.fullmatch(r"TTLCache\((-?\d+)\)", line)
            if not m:
                raise SystemExit("bad op: " + line)
            obj = TTLCache(int(m.group(1)))
            outs.append("null")
        elif line.startswith("put("):
            m = re.fullmatch(r"put\((-?\d+),\s*(-?\d+),\s*(-?\d+)\)", line)
            obj.put(int(m.group(1)), int(m.group(2)), int(m.group(3)))
            outs.append("null")
        elif line.startswith("get("):
            m = re.fullmatch(r"get\((-?\d+),\s*(-?\d+)\)", line)
            outs.append(str(obj.get(int(m.group(1)), int(m.group(2)))))
        elif line.startswith("purge("):
            m = re.fullmatch(r"purge\((-?\d+)\)", line)
            outs.append(str(obj.purge(int(m.group(1)))))
        elif line.startswith("size("):
            m = re.fullmatch(r"size\(\)", line)
            if not m:
                raise SystemExit("bad op: " + line)
            outs.append(str(obj.size()))
        else:
            raise SystemExit("bad op: " + line)
    return outs


text = sys.stdin.read()
if not text.strip():
    raise SystemExit(0)
print("\n".join(run(text.split("\n"))))
