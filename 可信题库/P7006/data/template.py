import re
import sys


def run(lines):
    outs = []
    obj = None
    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        if line == "ClusterPool()":
            obj = ClusterPool()
            outs.append("null")
        elif line.startswith("addNode("):
            m = re.fullmatch(r"addNode\((-?\d+),\s*(-?\d+)\)", line)
            if not m:
                raise SystemExit("bad op: " + line)
            outs.append("true" if obj.addNode(int(m.group(1)), int(m.group(2))) else "false")
        elif line.startswith("removeNode("):
            m = re.fullmatch(r"removeNode\((-?\d+)\)", line)
            if not m:
                raise SystemExit("bad op: " + line)
            outs.append("true" if obj.removeNode(int(m.group(1))) else "false")
        elif line.startswith("submit("):
            m = re.fullmatch(r"submit\((-?\d+),\s*(-?\d+)\)", line)
            if not m:
                raise SystemExit("bad op: " + line)
            outs.append(str(obj.submit(int(m.group(1)), int(m.group(2)))))
        elif line.startswith("kill("):
            m = re.fullmatch(r"kill\((-?\d+)\)", line)
            if not m:
                raise SystemExit("bad op: " + line)
            outs.append("true" if obj.kill(int(m.group(1))) else "false")
        elif line.startswith("usedOf("):
            m = re.fullmatch(r"usedOf\((-?\d+)\)", line)
            if not m:
                raise SystemExit("bad op: " + line)
            outs.append(str(obj.usedOf(int(m.group(1)))))
        elif line.startswith("freeOf("):
            m = re.fullmatch(r"freeOf\((-?\d+)\)", line)
            if not m:
                raise SystemExit("bad op: " + line)
            outs.append(str(obj.freeOf(int(m.group(1)))))
        elif line.startswith("jobNode("):
            m = re.fullmatch(r"jobNode\((-?\d+)\)", line)
            if not m:
                raise SystemExit("bad op: " + line)
            outs.append(str(obj.jobNode(int(m.group(1)))))
        else:
            raise SystemExit("bad op: " + line)
    return outs


text = sys.stdin.read()
if not text.strip():
    raise SystemExit(0)
print("\n".join(run(text.split("\n"))))
