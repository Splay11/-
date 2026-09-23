import re
import sys


def run(lines):
    outs = []
    obj = None
    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        if line.startswith("ParkingLane("):
            m = re.fullmatch(r"ParkingLane\((-?\d+)\)", line)
            obj = ParkingLane(int(m.group(1)))
            outs.append("null")
        elif line.startswith("arrive("):
            m = re.fullmatch(r"arrive\((-?\d+)\)", line)
            outs.append("true" if obj.arrive(int(m.group(1))) else "false")
        elif line.startswith("admit("):
            outs.append("true" if obj.admit() else "false")
        elif line.startswith("depart("):
            m = re.fullmatch(r"depart\((-?\d+)\)", line)
            outs.append(str(obj.depart(int(m.group(1)))))
        elif line.startswith("undo("):
            outs.append("true" if obj.undo() else "false")
        elif line.startswith("front("):
            outs.append(str(obj.front()))
        elif line.startswith("waiting("):
            outs.append(str(obj.waiting()))
        elif line.startswith("size("):
            outs.append(str(obj.size()))
        else:
            raise SystemExit("bad op: " + line)
    return outs


text = sys.stdin.read()
if not text.strip():
    raise SystemExit(0)
print("\n".join(run(text.split("\n"))))
