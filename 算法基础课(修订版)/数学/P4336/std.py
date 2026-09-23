import sys
import math

def main():
    # 读取四个正整数 a b c d
    data = sys.stdin.read().strip().split()
    a, b, c, d = map(int, data[:4])

    # 比例相等：空白为 0/1
    if a * d == b * c:
        print("0/1")
        return

    # 计算“画作占屏幕面积”的分数 p/q
    if a * d > b * c:
        # 屏幕更宽：以高贴合
        p, q = c * b, a * d
    else:
        # 屏幕更窄：以宽贴合
        p, q = a * d, b * c

    # 空白比例 = (q - p) / q
    num = q - p
    den = q
    g = math.gcd(num, den)
    num //= g
    den //= g

    print(f"{num}/{den}")

if __name__ == "__main__":
    main()
