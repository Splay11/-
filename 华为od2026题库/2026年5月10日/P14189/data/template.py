import sys
import ast

# 模板只负责读取输入、调用用户实现并输出结果
def 解析输入(文本):
    文本 = 文本.strip()
    if not 文本:
        return []

    # 优先使用 ast.literal_eval 解析逗号分隔或列表形式输入
    try:
        数据 = ast.literal_eval(文本)
        if isinstance(数据, (list, tuple)):
            return [int(x) for x in 数据]
        return [int(数据)]
    except Exception:
        # 兼容普通逗号分隔、括号包裹等形式
        for 字符 in "[](){},":
            文本 = 文本.replace(字符, " ")
        return [int(x) for x in 文本.split()]


def main():
    参数 = 解析输入(sys.stdin.read())
    capacity, align, read_index, write_index, pkt_size = 参数[:5]

    答案 = Solution().calcWriteIndex(
        capacity,
        align,
        read_index,
        write_index,
        pkt_size
    )
    print(答案)


if __name__ == "__main__":
    main()
