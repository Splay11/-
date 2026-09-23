import json
import re
import sys


def fmt_files(arr):
    return json.dumps(arr)


def run(lines):
    outs = []
    obj = None
    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        m = re.fullmatch(r"FileLogger\((-?\d+),\s*(-?\d+)\)", line)
        if m:
            obj = FileLogger(int(m.group(1)), int(m.group(2)))
            outs.append("null")
        elif line.startswith("putLog("):
            m = re.fullmatch(r"putLog\((-?\d+),\s*(-?\d+)\)", line)
            if not m:
                raise SystemExit("bad op: " + line)
            outs.append(str(obj.putLog(int(m.group(1)), int(m.group(2)))))
        elif line == "listFiles()":
            outs.append(fmt_files(obj.listFiles()))
        elif line == "totalSize()":
            outs.append(str(obj.totalSize()))
        else:
            raise SystemExit("bad op: " + line)
    return outs


text = sys.stdin.read()
if not text.strip():
    raise SystemExit(0)
print("\n".join(run(text.split("\n"))))
