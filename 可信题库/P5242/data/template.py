import re
import sys


def run(lines):
    outs = []
    obj = None
    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        if line.startswith("ParkingLot("):
            m = re.fullmatch(r"ParkingLot\((\d+)\)", line)
            obj = ParkingLot(int(m.group(1)))
            outs.append("null")
        elif line.startswith("reserve("):
            m = re.fullmatch(r"reserve\((-?\d+),\s*(-?\d+),\s*(-?\d+)\)", line)
            outs.append(str(obj.reserve(int(m.group(1)), int(m.group(2)), int(m.group(3)))))
        elif line.startswith("cancel("):
            m = re.fullmatch(r"cancel\((-?\d+)\)", line)
            outs.append("true" if obj.cancel(int(m.group(1))) else "false")
        elif line.startswith("spotOf("):
            m = re.fullmatch(r"spotOf\((-?\d+)\)", line)
            outs.append(str(obj.spotOf(int(m.group(1)))))
        elif line.startswith("busyCount("):
            m = re.fullmatch(r"busyCount\((-?\d+)\)", line)
            outs.append(str(obj.busyCount(int(m.group(1)))))
        else:
            raise SystemExit("bad op: " + line)
    return outs


text = sys.stdin.read()
if not text.strip():
    raise SystemExit(0)
print("\n".join(run(text.split("\n"))))
