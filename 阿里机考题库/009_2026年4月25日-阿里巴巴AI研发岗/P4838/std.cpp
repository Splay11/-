#include <bits/stdc++.h>
using namespace std;

long long countLeq(const vector<long long>& load, long long limit) {
    int length = load.size();

    // r 为右端点开区间，当前窗口为 [l, r)
    int r = 0;

    // windowSum 为当前窗口内负载之和
    long long windowSum = 0;

    // curScore 为当前窗口的段累计分
    long long curScore = 0;

    long long cnt = 0;

    for (int l = 0; l < length; l++) {
        // 尽量右扩窗口，保证段累计分不超过 limit
        while (r < length) {
            long long newSum = windowSum + load[r];
            long long newScore = curScore + newSum;

            if (newScore > limit) {
                break;
            }

            windowSum = newSum;
            curScore = newScore;
            r++;
        }

        cnt += r - l;

        if (r > l) {
            curScore -= 1LL * (r - l) * load[l];
            windowSum -= load[l];
        } else {
            r = l + 1;
        }
    }

    return cnt;
}

long long kthScore(const vector<long long>& load, long long rank) {
    // 上界取整段 [1, length] 的段累计分
    long long running = 0;
    long long high = 0;

    for (long long x : load) {
        running += x;
        high += running;
    }

    long long low = 0;

    // 二分最小的 ans，使 score <= ans 的区间数不少于 rank
    while (low < high) {
        long long mid = low + (high - low) / 2;

        if (countLeq(load, mid) >= rank) {
            high = mid;
        } else {
            low = mid + 1;
        }
    }

    return low;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int tc;
    cin >> tc;

    while (tc--) {
        int length;
        long long rank;
        cin >> length >> rank;

        vector<long long> load(length);
        for (int i = 0; i < length; i++) {
            cin >> load[i];
        }

        cout << kthScore(load, rank) << '\n';
    }

    return 0;
}
