import sys


def main():
    # 读取一行 IPv4 地址，保留除换行符以外的原始内容，避免误删非法空格
    ip = sys.stdin.readline()
    if ip.endswith("\n"):
        ip = ip[:-1]
    if ip.endswith("\r"):
        ip = ip[:-1]

    # 调用用户实现的函数并输出结果
    ans = Solution().classifyIPv4(ip)
    print(ans)


if __name__ == "__main__":
    main()
