#include <iostream>
#include <vector>
using namespace std;

int nGlobal, WGlobal, TGlobal;
long long ans;
vector<int> v, w;

void dfs(int i, int vol, int trig, long long cur) {
    if (i == nGlobal) {
        if (cur > ans) {
            ans = cur;
        }
        return;
    }
    dfs(i + 1, vol, trig, cur);
    int cost = trig ? (v[i] / 2) : v[i];
    int nvol = vol + cost;
    if (nvol <= WGlobal) {
        int ntrig = (trig || nvol >= TGlobal) ? 1 : 0;
        dfs(i + 1, nvol, ntrig, cur + w[i]);
    }
}

long long maxValue(int n, int W, int T, const vector<int>& vv, const vector<int>& ww) {
    nGlobal = n;
    WGlobal = W;
    TGlobal = T;
    v = vv;
    w = ww;
    ans = 0;
    dfs(0, 0, 0, 0);
    return ans;
}

int main() {
    int n, W, T;
    cin >> n >> W >> T;
    vector<int> v(n), w(n);
    for (int i = 0; i < n; i++) {
        cin >> v[i] >> w[i];
    }
    cout << maxValue(n, W, T, v, w) << "\n";
    return 0;
}
