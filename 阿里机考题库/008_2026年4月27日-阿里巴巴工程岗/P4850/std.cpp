#include <bits/stdc++.h>
using namespace std;

// 在化简后的品类序列上求最长奇回文半径
int oddPalindromeRadius(const vector<int>& labels) {
    int n = labels.size();
    vector<int> radius(n);
    int left = 0, right = -1;
    int best = 0;

    for (int i = 0; i < n; i++) {
        int k;
        if (i > right) {
            k = 1;
        } else {
            k = min(radius[left + right - i], right - i + 1);
        }

        while (i - k >= 0 && i + k < n && labels[i - k] == labels[i + k]) {
            k++;
        }

        radius[i] = k;
        best = max(best, k);

        if (i + k - 1 > right) {
            left = i - k + 1;
            right = i + k - 1;
        }
    }

    return best;
}

int maxClearances(int n, const vector<int>& categories) {
    vector<int> stack;

    // 模拟不补货箱时的全部配对清除
    for (int cat : categories) {
        if (!stack.empty() && stack.back() == cat) {
            stack.pop_back();
        } else {
            stack.push_back(cat);
        }
    }

    int reducedLen = stack.size();
    int base = (n - reducedLen) / 2;

    // 已全部清完，补入单个货箱无法产生新清除
    if (reducedLen == 0) {
        return base;
    }

    int extra = oddPalindromeRadius(stack);
    return base + extra;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T;
    cin >> T;

    while (T--) {
        int n;
        cin >> n;

        vector<int> categories(n);
        for (int i = 0; i < n; i++) {
            cin >> categories[i];
        }

        cout << maxClearances(n, categories) << '\n';
    }

    return 0;
}
