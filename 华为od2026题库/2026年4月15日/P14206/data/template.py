# -*- coding: utf-8 -*-
# HydroOJ 函数题模式 Python 模板文件
# 说明：
# 1. 本文件负责输入解析、调用用户实现的函数、输出结果
# 2. 用户需要在 user.py 中实现 Solution 类的 mergeLogs 方法
# 3. 输入格式示例：
#    ["/api/user","/api/user","/api/order"],[100,200,150]

import sys
import ast


def main():
    data = sys.stdin.read().strip()

    if not data:
        paths = []
        response_times = []
    else:
        paths, response_times = ast.literal_eval("[" + data + "]")

    ans = Solution().mergeLogs(paths, response_times)

    # 使用紧凑格式输出（无空格）
    import json
    print(json.dumps(ans, separators=(",", ":")))


if __name__ == "__main__":
    main()
