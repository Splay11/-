// 从下标 0 按当前值的质因数左右跳，判断能否到达最后一个下标
#include <iostream>
#include <queue>
#include <sstream>
#include <string>
#include <vector>
using namespace std;

// 分解 x 的全部不同质因数。1 没有质因数。
vector<int> primeFactors(int x) {
    vector<int> factors;
    if (x <= 1) {
        return factors;
    }
    if (x % 2 == 0) {
        factors.push_back(2);
        while (x % 2 == 0) {
            x /= 2;
        }
    }
    for (int d = 3; 1LL * d * d <= x; d += 2) {
        if (x % d == 0) {
            factors.push_back(d);
            while (x % d == 0) {
                x /= d;
            }
        }
    }
    // 剩下大于 1 的就是最后一个质数
    if (x > 1) {
        factors.push_back(x);
    }
    return factors;
}

// 从下标 0 出发 BFS，边为 ±质因数且不越界
bool canReach(const vector<int>& seq) {
    int m = (int)seq.size();
    // 只有一个位置时，起点就是终点
    if (m == 1) {
        return true;
    }
    vector<char> vis(m, 0);
    queue<int> q;
    vis[0] = 1;
    q.push(0);
    while (!q.empty()) {
        int p = q.front();
        q.pop();
        vector<int> factors = primeFactors(seq[p]);
        for (int d : factors) {
            int cand[2] = {p + d, p - d};
            for (int nxt : cand) {
                if (nxt < 0 || nxt >= m || vis[nxt]) {
                    continue;
                }
                if (nxt == m - 1) {
                    return true;
                }
                vis[nxt] = 1;
                q.push(nxt);
            }
        }
    }
    return false;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    // 一行空格分隔的整个序列
    string line;
    getline(cin, line);
    stringstream ss(line);
    vector<int> seq;
    int x;
    while (ss >> x) {
        seq.push_back(x);
    }
    cout << (canReach(seq) ? "true" : "false") << '\n';
    return 0;
}
