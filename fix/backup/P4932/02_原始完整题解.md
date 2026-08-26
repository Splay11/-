## 解题思路

将朋友按金币数从小到大排序，房子按价格从小到大排序。

依次处理每个朋友：

* 把当前朋友能买得起的所有房子加入最大堆，堆中按舒适度排序。
* 当前朋友选择堆中舒适度最大的房子购买。
* 该房子被购买后从堆中删除。

这样做是正确的，因为金币少的朋友能买的房子集合更小，应该优先安排；金币多的朋友能买金币少的朋友能买的所有房子，所以不会因为先满足金币少的人而损失最优性。

若当前朋友选择了当前可买房子中舒适度最大的房子：

* 如果最优方案中这个房子没人买，可以直接换给当前朋友，答案不会变差。
* 如果最优方案中这个房子被后面的朋友买了，由于后面的朋友金币不少于当前朋友，可以交换两人购买的房子，仍然合法，答案不变差。

因此贪心成立。

需要注意：按题意样例中两个朋友都可以买一个舒适度为 $2$ 的房子，最大和应为 $4$，题面给出的输出 $2$ 疑似有误。以下代码按“最大舒适度之和”实现。

## 复杂度分析

设朋友数为 $n$，房子数为 $m$。

排序复杂度为 $O(n \log n + m \log m)$。

每个房子最多入堆一次、出堆一次，因此堆操作复杂度为 $O(m \log m)$。

总时间复杂度为：

$$
O(n \log n + m \log m)
$$

空间复杂度为：

$$
O(m)
$$

可以满足 $1 \le n,m \le 2 \times 10^5$ 的数据范围。

## 代码实现

### Python

```python
import sys
import heapq


def max_comfort_sum(coins, houses):
    # 将朋友按金币数从小到大排序
    coins.sort()

    # 将房子按价格从小到大排序，house = (price, comfort)
    houses.sort()

    heap = []
    ans = 0
    j = 0
    m = len(houses)

    # 依次处理每个朋友
    for money in coins:
        # 把当前朋友买得起的房子全部加入最大堆
        while j < m and houses[j][0] <= money:
            price, comfort = houses[j]
            heapq.heappush(heap, -comfort)
            j += 1

        # 当前朋友购买舒适度最高的可购买房子
        if heap:
            ans += -heapq.heappop(heap)

    return ans


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    n, m = data[0], data[1]

    coins = data[2:2 + n]

    houses = []
    idx = 2 + n
    for _ in range(m):
        comfort = data[idx]
        price = data[idx + 1]
        houses.append((price, comfort))
        idx += 2

    print(max_comfort_sum(coins, houses))


if __name__ == "__main__":
    main()
```

### Java

```java
import java.util.*;

public class Main {

    public static long maxComfortSum(long[] coins, long[][] houses) {
        // 将朋友按金币数从小到大排序
        Arrays.sort(coins);

        // 将房子按价格从小到大排序
        Arrays.sort(houses, new Comparator<long[]>() {
            public int compare(long[] o1, long[] o2) {
                return Long.compare(o1[0], o2[0]);
            }
        });

        // 最大堆，存储当前可以买的房子的舒适度
        PriorityQueue<Long> heap = new PriorityQueue<>(Collections.reverseOrder());

        long ans = 0;
        int j = 0;
        int m = houses.length;

        // 依次处理每个朋友
        for (long money : coins) {
            // 把当前朋友买得起的房子全部加入最大堆
            while (j < m && houses[j][0] <= money) {
                heap.offer(houses[j][1]);
                j++;
            }

            // 当前朋友购买舒适度最高的可购买房子
            if (!heap.isEmpty()) {
                ans += heap.poll();
            }
        }

        return ans;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        int n = sc.nextInt();
        int m = sc.nextInt();

        long[] coins = new long[n];
        for (int i = 0; i < n; i++) {
            coins[i] = sc.nextLong();
        }

        long[][] houses = new long[m][2];
        for (int i = 0; i < m; i++) {
            long comfort = sc.nextLong();
            long price = sc.nextLong();

            // houses[i][0] 表示价格，houses[i][1] 表示舒适度
            houses[i][0] = price;
            houses[i][1] = comfort;
        }

        System.out.println(maxComfortSum(coins, houses));
    }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

long long maxComfortSum(vector<long long>& coins, vector<pair<long long, long long>>& houses) {
    // 将朋友按金币数从小到大排序
    sort(coins.begin(), coins.end());

    // 将房子按价格从小到大排序，pair = {价格, 舒适度}
    sort(houses.begin(), houses.end());

    // 最大堆，存储当前可以买的房子的舒适度
    priority_queue<long long> heap;

    long long ans = 0;
    int j = 0;
    int m = houses.size();

    // 依次处理每个朋友
    for (long long money : coins) {
        // 把当前朋友买得起的房子全部加入最大堆
        while (j < m && houses[j].first <= money) {
            heap.push(houses[j].second);
            j++;
        }

        // 当前朋友购买舒适度最高的可购买房子
        if (!heap.empty()) {
            ans += heap.top();
            heap.pop();
        }
    }

    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    cin >> n >> m;

    vector<long long> coins(n);
    for (int i = 0; i < n; i++) {
        cin >> coins[i];
    }

    vector<pair<long long, long long>> houses;
    for (int i = 0; i < m; i++) {
        long long comfort, price;
        cin >> comfort >> price;

        // 存储为 {价格, 舒适度}，方便按价格排序
        houses.push_back({price, comfort});
    }

    cout << maxComfortSum(coins, houses) << '\n';

    return 0;
}
```