#include <iostream>
#include <vector>
using namespace std;

// 沿当前方向扫描，能揭就揭；整趟没有进展则失败，否则掉头继续
int min_turns(const vector<int> &w) {
    int n = (int)w.size();
    vector<char> opened(n, 0);
    int keys = 0;
    int done = 0;
    int ans = 0;
    int d = 1;
    int i = 0;
    while (done < n) {
        int gained = 0;
        // 沿当前方向走到尽头，路过能揭的彩门就揭
        while (i >= 0 && i < n) {
            if (!opened[i] && keys >= w[i]) {
                opened[i] = 1;
                keys++;
                done++;
                gained++;
            }
            i += d;
        }
        if (done == n) {
            return ans;
        }
        // 这一趟一扇都没揭开，剩下的阈值永远够不着
        if (gained == 0) {
            return -1;
        }
        // 走到尽头后换向，从端点外再踏回数组
        d = -d;
        i += d;
        ans++;
    }
    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int q;
    cin >> q;
    while (q--) {
        int m;
        cin >> m;
        vector<int> w(m);
        for (int j = 0; j < m; j++) {
            cin >> w[j];
        }
        cout << min_turns(w) << "\n";
    }
    return 0;
}
