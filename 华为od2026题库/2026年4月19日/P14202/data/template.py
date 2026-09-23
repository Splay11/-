import sys
import ast


def 读取输入():
    数据 = sys.stdin.read().strip()
    if not 数据:
        return ""
    try:
        值 = ast.literal_eval(数据)
        if isinstance(值, str):
            return 值
    except Exception:
        pass
    if len(数据) >= 2 and 数据[0] == '"' and 数据[-1] == '"':
        return 数据[1:-1]
    return 数据


def main():
    sortResolutions = 读取输入()
    result = Solution().sort(sortResolutions)
    if result is None:
        result = ""
    sys.stdout.write(str(result))


if __name__ == "__main__":
    main()
