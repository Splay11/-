from collections import defaultdict

jobNum = 0
times = []
mutex = defaultdict(set)
ans = 1
cost = float('inf')

def check(i, usd):
    for u in usd:
        if i in mutex[u] or u in mutex[i]:
            return False
    return True

def dfs(i, usd, time):
    global ans, cost
    # 停止条件
    if i >= jobNum:
        if ans <= len(usd):
            if ans < len(usd):
                ans = len(usd)
                cost = time
            elif ans == len(usd):
                if time < cost:
                    cost = time
        return

    if len(usd) + jobNum - i + 1 < ans:
        return

    # 不选择当前任务
    dfs(i + 1, usd, time)

    # 选择当前任务
    if check(i, usd):
        usd.add(i)
        dfs(i + 1, usd, time + times[i])
        usd.remove(i)

def main():
    global jobNum, times, mutex, ans, cost
    jobNum = int(input())
    times = list(map(int, input().split()))

    mutexNum = int(input())
    for _ in range(mutexNum):
        a, b = map(int, input().split())
        a -= 1  # 转换为0基索引
        b -= 1  # 转换为0基索引
        mutex[a].add(b)
        mutex[b].add(a)

    usd = set()
    dfs(0, usd, 0)

    print(cost)

if __name__ == "__main__":
    main()
