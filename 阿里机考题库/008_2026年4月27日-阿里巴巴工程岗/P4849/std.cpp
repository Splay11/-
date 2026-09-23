#include <bits/stdc++.h>
using namespace std;

const long long MOD = 1000000007LL;

long long segmentContribution(long long len) {
    // 长度为 len 的合规差分段贡献 len*(len-1)*(len+1)/6
    return len * (len - 1) * (len + 1) / 6;
}

long long countTurnPoints(int m, vector<long long>& readings) {
    if (m < 3) {
        return 0;
    }

    long long total = 0;
    long long runLen = 1; // 当前合规差分段长度

    for (int i = 1; i < m - 1; i++) {
        long long deltaLeft = readings[i] - readings[i - 1];
        long long deltaRight = readings[i + 1] - readings[i];
        // 相邻差分异号或含零，说明该内部测点是拐点
        if (deltaLeft * deltaRight <= 0) {
            runLen++;
        } else {
            total = (total + segmentContribution(runLen)) % MOD;
            runLen = 1;
        }
    }

    total = (total + segmentContribution(runLen)) % MOD;
    return total;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T;
    cin >> T;

    while (T--) {
        int m;
        cin >> m;

        vector<long long> readings(m);
        for (int i = 0; i < m; i++) {
            cin >> readings[i];
        }

        cout << countTurnPoints(m, readings) << '\n';
    }

    return 0;
}
