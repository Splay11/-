#include <iostream>
#include <vector>
using namespace std;

const long long LIM = 10000000000000000LL;

// 构造长度为 length、数位和为 digitSum 的最小十进制数
long long makeMinNumber(int length, int digitSum) {
    int first = digitSum - 9 * (length - 1);
    if (first < 1) {
        first = 1;
    }
    if (first > 9 || first > digitSum) {
        return -1;
    }
    int rest = digitSum - first;
    vector<int> digits(length, 0);
    digits[0] = first;
    // 余数尽量放到右边，左边才能尽量小
    for (int i = length - 1; i >= 1; i--) {
        int take = rest < 9 ? rest : 9;
        digits[i] = take;
        rest -= take;
    }
    if (rest != 0) {
        return -1;
    }
    long long value = 0;
    for (int i = 0; i < length; i++) {
        value = value * 10 + digits[i];
    }
    return value;
}

// 从小到大枚举位数 L，第一个合法编号就是最小的
long long minCode(int w) {
    for (int length = 1; length <= 17; length++) {
        if (w % length != 0) {
            continue;
        }
        int digitSum = w / length;
        if (digitSum < 1 || digitSum > 9 * length) {
            continue;
        }
        if (length == 17) {
            // 闭区间上界 10^16 是唯一的 17 位数
            if (digitSum == 1) {
                return LIM;
            }
            continue;
        }
        long long value = makeMinNumber(length, digitSum);
        if (value < 0 || value > LIM) {
            continue;
        }
        return value;
    }
    return -1;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(0);

    int q;
    cin >> q;
    vector<long long> ans;
    ans.reserve(q);
    for (int i = 0; i < q; i++) {
        int w;
        cin >> w;
        ans.push_back(minCode(w));
    }
    for (int i = 0; i < q; i++) {
        if (i) {
            cout << ' ';
        }
        cout << ans[i];
    }
    cout << "\n";
    return 0;
}
