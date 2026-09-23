import re
import sys


def run(lines):
    outs = []
    obj = None
    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        if line.startswith("JobQueueSys("):
            m = re.fullmatch(r"JobQueueSys\(\)", line)
            if not m:
                raise SystemExit("bad op: " + line)
            obj = JobQueueSys()
            outs.append("null")
        elif line.startswith("submit("):
            m = re.fullmatch(r"submit\((-?\d+),\s*(-?\d+)\)", line)
            outs.append("true" if obj.submit(int(m.group(1)), int(m.group(2))) else "false")
        elif line.startswith("cancel("):
            m = re.fullmatch(r"cancel\((-?\d+)\)", line)
            outs.append("true" if obj.cancel(int(m.group(1))) else "false")
        elif line.startswith("popJob("):
            m = re.fullmatch(r"popJob\(\)", line)
            if not m:
                raise SystemExit("bad op: " + line)
            outs.append(str(obj.popJob()))
        elif line.startswith("peekJob("):
            m = re.fullmatch(r"peekJob\(\)", line)
            if not m:
                raise SystemExit("bad op: " + line)
            outs.append(str(obj.peekJob()))
        else:
            raise SystemExit("bad op: " + line)
    return outs


text = sys.stdin.read()
if not text.strip():
    raise SystemExit(0)
print("\n".join(run(text.split("\n"))))
