import sys
import re


def run(lines):
    outs = []
    obj = None
    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        if line == "LogSystem()":
            obj = LogSystem()
            outs.append("null")
        elif line.startswith("log("):
            m = re.fullmatch(r'log\("((?:\\.|[^"\\])*)"\)', line)
            if not m:
                # 简单路径：log("...") 无转义
                m2 = re.fullmatch(r'log\("(.*)"\)', line)
                msg = m2.group(1) if m2 else ""
            else:
                msg = m.group(1)
            outs.append('"' + obj.log(msg) + '"')
        elif line.startswith("enter("):
            m = re.fullmatch(r"enter\((\d+)\s*,\s*(true|false)\)", line)
            span_id = int(m.group(1))
            inherit = m.group(2) == "true"
            obj.enter(span_id, inherit)
            outs.append("null")
        elif line.startswith("leave("):
            m = re.fullmatch(r"leave\((\d+)\)", line)
            obj.leave(int(m.group(1)))
            outs.append("null")
        else:
            raise SystemExit("bad op: " + line)
    return outs


text = sys.stdin.read()
if not text.strip():
    raise SystemExit(0)
# 保留中间空行语义：按行切，最后一行后可能无换行
lines = text.split("\n")
# 去掉因末尾无换行产生的问题：split 已正确；过滤纯空行
print("\n".join(run(lines)))
