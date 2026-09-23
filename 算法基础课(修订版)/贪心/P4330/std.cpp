#include <iostream>
#include <vector>
#include <queue>

// 使用 pair 来存储 {价格, 数量}
using P = std::pair<long long, int>;

int main() {
    // 加速 C++ IO
    std::ios_base::sync_with_stdio(false);
    std::cin.tie(NULL);

    int n, m, x;
    std::cin >> n >> m >> x;

    std::vector<long long> a(n);
    for (int i = 0; i < n; ++i) {
        std::cin >> a[i];
    }

    // orders_due[i] 存储最晚发货日期为第 i+1 天的订单数量
    std::vector<int> orders_due(n, 0);
    for (int i = 0; i < m; ++i) {
        int b;
        std::cin >> b;
        // 转换为 0-based 索引
        orders_due[b - 1]++;
    }

    // 最小优先队列（小顶堆），存储可用的发货槽位 {价格, 数量}
    // std::greater<P> 使其按 pair 的第一个元素（价格）升序排序
    std::priority_queue<P, std::vector<P>, std::greater<P>> pq;

    long long total_cost = 0;

    // 从第 1 天到第 n 天遍历
    for (int i = 0; i < n; ++i) {
        // 将当天的发货槽位加入优先队列
        pq.push({a[i], x});

        // 获取当天必须发货的订单数量
        int orders_to_ship = orders_due[i];

        // 为这些订单分配成本最低的槽位
        while (orders_to_ship > 0) {
            // 取出当前最便宜的槽位信息
            P top = pq.top();
            pq.pop();
            long long cost = top.first;
            int count = top.second;

            // 决定使用多少个这种价格的槽位
            int num_to_use = std::min(orders_to_ship, count);

            // 累加成本
            total_cost += num_to_use * cost;
            
            // 更新剩余需要发货的订单数量
            orders_to_ship -= num_to_use;
            
            // 如果这种价格的槽位还有剩余，将其放回优先队列
            if (count > num_to_use) {
                pq.push({cost, count - num_to_use});
            }
        }
    }

    std::cout << total_cost << std::endl;

    return 0;
}
