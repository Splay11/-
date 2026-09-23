#include <iostream>
#include <vector>
using namespace std;

vector<int> threeDigitEvens(const vector<int>& digits) {
    // cnt[d] 表示数字 d 在数组里出现了几次
    int cnt[10] = {0};
    for (int d : digits) {
        cnt[d]++;
    }

    vector<int> res;
    // 百位从 1 开始枚举，天然排除了前导零
    for (int a = 1; a <= 9; a++) {
        if (cnt[a] == 0) continue;
        cnt[a]--;  // 用掉一个 a
        for (int b = 0; b <= 9; b++) {
            if (cnt[b] == 0) continue;
            cnt[b]--;  // 用掉一个 b
            // 个位只能是偶数，才能保证整个数是偶数
            for (int c = 0; c <= 8; c += 2) {
                if (cnt[c] == 0) continue;
                // 三个数位都够用，组成一个合法的三位偶数
                res.push_back(a * 100 + b * 10 + c);
            }
            cnt[b]++;  // 还回 b，继续试下一个十位
        }
        cnt[a]++;  // 还回 a，继续试下一个百位
    }

    // 三个数位都是从小到大枚举的，所以 res 已经是递增顺序；
    // 数位确定则整数唯一，因此不会出现重复
    return res;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    // 第一行：数组长度 n
    int n;
    cin >> n;
    // 第二行：n 个 0~9 的数字
    vector<int> digits(n);
    for (int i = 0; i < n; i++) {
        cin >> digits[i];
    }

    vector<int> ans = threeDigitEvens(digits);

    // 第一行输出个数 k
    cout << ans.size() << "\n";
    // 只有 k>0 时才输出第二行；k=0 时题面要求只输出一行 0
    if (!ans.empty()) {
        for (size_t i = 0; i < ans.size(); i++) {
            if (i) cout << " ";
            cout << ans[i];
        }
        cout << "\n";
    }
    return 0;
}
