#include <iostream>
#include <vector>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<int> p(n);
    for (int i = 0; i < n; i++) cin >> p[i];

    // 最小交换次数 = n - 环个数
    vector<char> vis(n, 0);
    int cycles = 0;
    for (int i = 0; i < n; i++) {
        if (vis[i]) continue;
        cycles++;
        int j = i;
        // 沿置换走完一个环
        while (!vis[j]) {
            vis[j] = 1;
            j = p[j] - 1;
        }
    }
    cout << n - cycles << '\n';
    return 0;
}
