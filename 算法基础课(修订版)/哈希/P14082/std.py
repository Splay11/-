from collections import Counter

def main():
    # 读取 n 和 Q 的值
    n, Q = map(int, input().split())
    
    # 读取口袋中的 n 个数字
    numbers = list(map(int, input().split()))
    
    # 使用 Counter 来统计每个数字的出现次数
    count_map = Counter(numbers)
    
    # 处理每个查询
    for _ in range(Q):
        # 读取查询的数字
        num = int(input())
        
        # 输出该数字出现的次数，如果没有出现过则输出 0
        print(count_map.get(num, 0))

if __name__ == "__main__":
    main()
