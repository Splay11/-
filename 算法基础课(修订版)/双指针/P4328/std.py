def countAtMostK(b, k):
    left = 0
    result = 0
    count = 0
    for right in range(len(b)):
        if b[right] == 1:
            count += 1
        while count > k:
            if b[left] == 1:
                count -= 1
            left += 1
        result += (right - left + 1)
    return result

def main():
    import sys
    # 读取第一行，整数序列 a
    a = list(map(int, sys.stdin.readline().split()))
    # 读取第二行，x 和 k
    x, k = map(int, sys.stdin.readline().split())
    # 将 a 映射为二进制数组 b，1 表示能被 x 整除，0 否则
    b = [1 if num % x == 0 else 0 for num in a]
    # 计算答案
    total = countAtMostK(b, k)
    if k > 0:
        total -= countAtMostK(b, k-1)
    print(total)

if __name__ == "__main__":
    main()
