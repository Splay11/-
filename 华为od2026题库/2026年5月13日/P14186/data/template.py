import ast
import json
import sys



def main():
    # 读取完整输入，兼容单行或多行格式
    data = sys.stdin.read().strip()
    if not data:
        print("[]")
        return

    # 输入格式为：n,k,packets
    # 通过补一层圆括号，将其转成一个三元组再解析
    n, k, packets = ast.literal_eval("(" + data + ")")

    # 调用用户实现的核心函数
    result = Solution().processPackets(int(n), int(k), packets)

    # 按题目要求输出紧凑格式
    print(json.dumps(result, ensure_ascii=False, separators=(",", ":")))


if __name__ == "__main__":
    main()
