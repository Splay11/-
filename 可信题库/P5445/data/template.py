import re
import sys


def run(lines):
    outs = []
    obj = None
    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        if line.startswith("PickupDesk("):
            obj = PickupDesk()
            outs.append("null")
        elif line.startswith("order("):
            m = re.fullmatch(r"order\((-?\d+)\)", line)
            outs.append("true" if obj.order(int(m.group(1))) else "false")
        elif line.startswith("serve("):
            outs.append(str(obj.serve()))
        elif line.startswith("waiting("):
            outs.append(str(obj.waiting()))
        else:
            raise SystemExit("bad op: " + line)
    return outs


text = sys.stdin.read()
if not text.strip():
    raise SystemExit(0)
print("\n".join(run(text.split("\n"))))
