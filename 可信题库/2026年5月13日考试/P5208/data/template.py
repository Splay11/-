import ast
import re
import sys


def fmt_list(a):
    if not a:
        return "[]"
    return "[" + ", ".join(str(x) for x in a) + "]"


def run(lines):
    outs = []
    obj = None
    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        if line.startswith("GCSystem("):
            m = re.fullmatch(r"GCSystem\((\d+)\)", line)
            obj = GCSystem(int(m.group(1)))
            outs.append("null")
        elif line.startswith("createObject("):
            m = re.fullmatch(r"createObject\((\d+)\)", line)
            obj.createObject(int(m.group(1)))
            outs.append("null")
        elif line.startswith("markObjects("):
            inner = line[len("markObjects(") : -1]
            ids = ast.literal_eval(inner)
            obj.markObjects(ids)
            outs.append("null")
        elif line.startswith("manualGC("):
            m = re.fullmatch(r"manualGC\((\d+)\)", line)
            obj.manualGC(int(m.group(1)))
            outs.append("null")
        elif line.startswith("getLiveObjects("):
            m = re.fullmatch(r"getLiveObjects\((\d+)\)", line)
            outs.append(fmt_list(obj.getLiveObjects(int(m.group(1)))))
        else:
            raise SystemExit("bad op: " + line)
    return outs


text = sys.stdin.read()
if not text.strip():
    raise SystemExit(0)
lines = text.split("\n")
print("\n".join(run(lines)))
