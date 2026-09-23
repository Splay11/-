# 读取多行输入并计算每行的和
import sys

def main():
    for line in sys.stdin:
        numbers = list(map(int, line.strip().split()))
        total = sum(numbers)
        print(total)

if __name__ == "__main__":
    main()
