import ast
import sys

def parse_nodes(text):
    text = text.strip()
    if not text:
        return []

    data = ast.literal_eval(text)

    # 标准输入：["1","#","2"] 或 [1,"#",2]
    if isinstance(data, list):
        # 兼容额外包一层：[["1","#","2"]]
        if len(data) == 1 and isinstance(data[0], list):
            data = data[0]

        # 统一转成字符串数组
        return [str(x) for x in data]

    # 兼容 tuple，例如 (["1","#","2"],)
    if isinstance(data, tuple):
        for item in data:
            if isinstance(item, list):
                return [str(x) for x in item]

        return [str(x) for x in data]

    # 兜底：如果输入被解析成单个整数，例如 1
    return [str(data)]


line = sys.stdin.read().strip()
nodes = parse_nodes(line)

print(Solution().maxDepth(nodes), end="")
