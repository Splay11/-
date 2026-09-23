import re
import sys


def run(lines):
    outs = []
    obj = None
    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        if line == "CertAuthority()":
            obj = CertAuthority()
            outs.append("null")
        elif line.startswith("issue("):
            m = re.fullmatch(r"issue\((-?\d+),\s*(-?\d+),\s*(-?\d+)\)", line)
            if not m:
                raise SystemExit("bad op: " + line)
            outs.append("true" if obj.issue(int(m.group(1)), int(m.group(2)), int(m.group(3))) else "false")
        elif line.startswith("revoke("):
            m = re.fullmatch(r"revoke\((-?\d+)\)", line)
            if not m:
                raise SystemExit("bad op: " + line)
            outs.append("true" if obj.revoke(int(m.group(1))) else "false")
        elif line.startswith("isValid("):
            m = re.fullmatch(r"isValid\((-?\d+),\s*(-?\d+)\)", line)
            if not m:
                raise SystemExit("bad op: " + line)
            outs.append("true" if obj.isValid(int(m.group(1)), int(m.group(2))) else "false")
        elif line.startswith("ttl("):
            m = re.fullmatch(r"ttl\((-?\d+),\s*(-?\d+)\)", line)
            if not m:
                raise SystemExit("bad op: " + line)
            outs.append(str(obj.ttl(int(m.group(1)), int(m.group(2)))))
        elif line.startswith("issuerOf("):
            m = re.fullmatch(r"issuerOf\((-?\d+)\)", line)
            if not m:
                raise SystemExit("bad op: " + line)
            outs.append(str(obj.issuerOf(int(m.group(1)))))
        elif line.startswith("rootOf("):
            m = re.fullmatch(r"rootOf\((-?\d+)\)", line)
            if not m:
                raise SystemExit("bad op: " + line)
            outs.append(str(obj.rootOf(int(m.group(1)))))
        else:
            raise SystemExit("bad op: " + line)
    return outs


text = sys.stdin.read()
if not text.strip():
    raise SystemExit(0)
print("\n".join(run(text.split("\n"))))
