import re
import sys


def run(lines):
    outs = []
    obj = None
    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        if line.startswith("ShardLeaseManager("):
            m = re.fullmatch(r"ShardLeaseManager\((\d+),\s*(\d+)\)", line)
            if not m:
                raise SystemExit("bad ctor: " + line)
            obj = ShardLeaseManager(int(m.group(1)), int(m.group(2)))
            outs.append("null")
        elif line.startswith("acquire("):
            m = re.fullmatch(r"acquire\((-?\d+),\s*(-?\d+),\s*(-?\d+),\s*(-?\d+)\)", line)
            if not m:
                raise SystemExit("bad op: " + line)
            outs.append(
                "true"
                if obj.acquire(int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4)))
                else "false"
            )
        elif line.startswith("renew("):
            m = re.fullmatch(r"renew\((-?\d+),\s*(-?\d+),\s*(-?\d+),\s*(-?\d+)\)", line)
            if not m:
                raise SystemExit("bad op: " + line)
            outs.append(
                "true"
                if obj.renew(int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4)))
                else "false"
            )
        elif line.startswith("release("):
            m = re.fullmatch(r"release\((-?\d+),\s*(-?\d+),\s*(-?\d+)\)", line)
            if not m:
                raise SystemExit("bad op: " + line)
            outs.append(
                "true" if obj.release(int(m.group(1)), int(m.group(2)), int(m.group(3))) else "false"
            )
        elif line.startswith("owner("):
            m = re.fullmatch(r"owner\((-?\d+),\s*(-?\d+)\)", line)
            if not m:
                raise SystemExit("bad op: " + line)
            outs.append(str(obj.owner(int(m.group(1)), int(m.group(2)))))
        elif line.startswith("heldCount("):
            m = re.fullmatch(r"heldCount\((-?\d+),\s*(-?\d+)\)", line)
            if not m:
                raise SystemExit("bad op: " + line)
            outs.append(str(obj.heldCount(int(m.group(1)), int(m.group(2)))))
        else:
            raise SystemExit("bad op: " + line)
    return outs


text = sys.stdin.read()
if not text.strip():
    raise SystemExit(0)
print("\n".join(run(text.split("\n"))))
