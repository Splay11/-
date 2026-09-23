from collections import defaultdict

def main():
    n = int(input())
    res = 0 
    count_left = defaultdict(int) 
    count_right = defaultdict(int) 
    a = list(map(int, input().split()))
    for i in a:
        count_right[i] += 1 # 统计每个元素的频率
    
    for i in a:
        t = i + 1 # 计算t = a[j] + 1
        res += count_left[t] * count_right[t] # 计算符合条件的三元组数量
        count_left[i] += 1 # 更新count_left
        count_right[i] -= 1 # 更新count_right
    
    print(res)

if __name__ == "__main__":
    main()
