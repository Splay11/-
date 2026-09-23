import sys
import ast


def 输出数组(arr):
    return "[" + ",".join(str(x) for x in arr) + "]"


def main():
    输入内容 = sys.stdin.read().strip()
    if not 输入内容:
        return

    n, sources, pipes = ast.literal_eval("(" + 输入内容 + ")")
    ans = Solution().findIsolatedStations(n, sources, pipes)
    print(输出数组(ans))


if __name__ == "__main__":
    main()
