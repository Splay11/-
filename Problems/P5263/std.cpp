#include <algorithm>
#include <iostream>
#include <numeric>
#include <vector>
using namespace std;

int minBottleneck(const vector<int>& layers, int m) {
    auto can = [&](long long limit) {
        int cnt = 1;
        long long s = 0;
        for (int x : layers) {
            if (s + x > limit) {
                cnt++;
                s = 0;
            }
            s += x;
        }
        return cnt <= m;
    };

    long long lo = *max_element(layers.begin(), layers.end());
    long long hi = accumulate(layers.begin(), layers.end(), 0LL);
    while (lo < hi) {
        long long mid = (lo + hi) / 2;
        if (can(mid)) {
            hi = mid;
        } else {
            lo = mid + 1;
        }
    }
    return (int)lo;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<int> layers(n);
    for (int i = 0; i < n; i++) {
        cin >> layers[i];
    }
    int m;
    cin >> m;
    cout << minBottleneck(layers, m) << '\n';
    return 0;
}
