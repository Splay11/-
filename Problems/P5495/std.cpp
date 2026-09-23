#include <iostream>
#include <vector>
using namespace std;

// 每人 each 颗时，每堆能切出 candies[i] / each 份；份数够 k 个小孩即可
bool canGive(const vector<int>& candies, long long k, int each) {
    if (each == 0) {
        return true;
    }
    long long got = 0;
    for (size_t i = 0; i < candies.size(); i++) {
        got += candies[i] / each;
        if (got >= k) {
            return true;
        }
    }
    return false;
}

// 答案越大越难满足，在 [0, max(candies)] 上二分最大可行值
int maxCandies(const vector<int>& candies, long long k) {
    int left = 0;
    int right = candies[0];
    for (size_t i = 1; i < candies.size(); i++) {
        if (candies[i] > right) {
            right = candies[i];
        }
    }
    while (left < right) {
        int mid = left + (right - left + 1) / 2;
        if (canGive(candies, k, mid)) {
            left = mid;
        } else {
            right = mid - 1;
        }
    }
    return left;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(0);

    // 第一行 n 与小孩数 k，第二行 n 堆糖果
    int n;
    long long k;
    cin >> n >> k;
    vector<int> candies(n);
    for (int i = 0; i < n; i++) {
        cin >> candies[i];
    }
    cout << maxCandies(candies, k) << "\n";
    return 0;
}
