#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n, m, d;
    long long k;
    cin >> n >> m >> d >> k;
    vector<long long> w(n + 1);
    for (int i = 1; i <= n; i++) {
        cin >> w[i];
    }
    for (int i = 0; i < m; i++) {
        int x;
        cin >> x;
        int left = x - d;
        if (left < 1) {
            left = 1;
        }
        int right = x - 1;
        long long thresh = w[x] - k;
        int cnt = 0;
        for (int j = left; j <= right; j++) {
            if (w[j] <= thresh) {
                cnt++;
            }
        }
        cout << cnt << "\n";
    }
    return 0;
}
