import re, sys

def run(lines):
    outs = []
    obj = None
    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        if line.startswith("LeaseManager("):
            m = re.fullmatch(r"LeaseManager\((-?\d+)\)", line)
            obj = LeaseManager(int(m.group(1)))
            outs.append("null")
        elif line.startswith("acquire("):
            m = re.fullmatch(r"acquire\((-?\d+),\s*(-?\d+),\s*(-?\d+)\)", line)
            outs.append("true" if obj.acquire(int(m.group(1)), int(m.group(2)), int(m.group(3))) else "false")
        elif line.startswith("renew("):
            m = re.fullmatch(r"renew\((-?\d+),\s*(-?\d+),\s*(-?\d+)\)", line)
            outs.append("true" if obj.renew(int(m.group(1)), int(m.group(2)), int(m.group(3))) else "false")
        elif line.startswith("release("):
            m = re.fullmatch(r"release\((-?\d+),\s*(-?\d+)\)", line)
            outs.append("true" if obj.release(int(m.group(1)), int(m.group(2))) else "false")
        elif line.startswith("holder("):
            m = re.fullmatch(r"holder\((-?\d+),\s*(-?\d+)\)", line)
            outs.append(str(obj.holder(int(m.group(1)), int(m.group(2)))))
        elif line.startswith("aliveCount("):
            m = re.fullmatch(r"aliveCount\((-?\d+)\)", line)
            outs.append(str(obj.aliveCount(int(m.group(1)))))
        else:
            raise SystemExit("bad op: " + line)
    return outs

text = sys.stdin.read()
if not text.strip():
    raise SystemExit(0)
print("\n".join(run(text.split("\n"))))
