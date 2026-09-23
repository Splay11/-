import re
import sys


def run(lines):
    outs = []
    obj = None
    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        if line.startswith("MicQueue("):
            obj = MicQueue()
            outs.append("null")
        elif line.startswith("enroll("):
            m = re.fullmatch(r"enroll\((-?\d+),\s*(-?\d+)\)", line)
            outs.append("true" if obj.enroll(int(m.group(1)), int(m.group(2))) else "false")
        elif line.startswith("nextPlay("):
            outs.append(str(obj.nextPlay()))
        elif line.startswith("boost("):
            m = re.fullmatch(r"boost\((-?\d+),\s*(-?\d+)\)", line)
            outs.append("true" if obj.boost(int(m.group(1)), int(m.group(2))) else "false")
        elif line.startswith("cancel("):
            m = re.fullmatch(r"cancel\((-?\d+)\)", line)
            outs.append("true" if obj.cancel(int(m.group(1))) else "false")
        elif line.startswith("waiting("):
            outs.append(str(obj.waiting()))
        else:
            raise SystemExit("bad op: " + line)
    return outs


text = sys.stdin.read()
if not text.strip():
    raise SystemExit(0)
print("\n".join(run(text.split("\n"))))
