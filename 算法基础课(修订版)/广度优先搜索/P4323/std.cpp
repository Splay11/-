#include <iostream>
#include <vector>
#include <queue>
#include <cstring>

using namespace std;

int main() {
    int n, k, m;
    cin >> n >> k >> m;

    vector<int> x(k);
    for (int i = 0; i < k; ++i) {
        cin >> x[i];
    }

    vector<int> y(m);
    for (int i = 0; i < m; ++i) {
        cin >> y[i];
    }

    // 最短路径数组
    vector<int> dist(n, -1);
    dist[0] = 0;  // 初始位置为 0，0 需要 0 次操作

    // BFS 队列
    queue<int> q;
    q.push(0);  // 从偏移量 0 开始

    while (!q.empty()) {
        int curr = q.front();
        q.pop();

        for (int i = 0; i < k; ++i) {
            int next = (curr + x[i]) % n;  // 新的偏移量
            if (dist[next] == -1) {  // 如果这个偏移量没有被访问过
                dist[next] = dist[curr] + 1;
                q.push(next);
            }
        }
    }

    // 对每个查询输出结果
    for (int i = 0; i < m; ++i) {
        cout << dist[y[i]] << endl;
    }

    return 0;
}
