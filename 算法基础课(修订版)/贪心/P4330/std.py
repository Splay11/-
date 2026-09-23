import heapq
import sys

def solve():
    # 读取输入
    n, m, x = map(int, sys.stdin.readline().split())
    prices = list(map(int, sys.stdin.readline().split()))
    deadlines = list(map(int, sys.stdin.readline().split()))

    # orders_due[i] 存储最晚发货日期为第 i+1 天的订单数量
    orders_due = [0] * n
    for d in deadlines:
        # 转换为 0-based 索引
        orders_due[d - 1] += 1
    
    # 最小优先队列（小顶堆），存储可用的发货槽位 (价格, 数量)
    pq = []
    
    total_cost = 0
    
    # 从第 1 天到第 n 天遍历
    for i in range(n):
        # 将当天的发货槽位加入优先队列
        # heapq 默认是小顶堆，元组会按第一个元素（价格）排序
        heapq.heappush(pq, (prices[i], x))
        
        # 获取当天必须发货的订单数量
        orders_to_ship = orders_due[i]
        
        # 为这些订单分配成本最低的槽位
        while orders_to_ship > 0:
            # 取出当前最便宜的槽位信息
            cost, count = heapq.heappop(pq)
            
            # 决定使用多少个这种价格的槽位
            num_to_use = min(orders_to_ship, count)
            
            # 累加成本
            total_cost += num_to_use * cost
            
            # 更新剩余需要发货的订单数量
            orders_to_ship -= num_to_use
            
            # 如果这种价格的槽位还有剩余，将其放回优先队列
            if count > num_to_use:
                heapq.heappush(pq, (cost, count - num_to_use))

    print(total_cost)

solve()
