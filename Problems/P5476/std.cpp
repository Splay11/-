#include <iostream>
#include <map>
#include <vector>
using namespace std;

const int MAXB = 1000000;

// 线性筛最小质因子，后面拆指纹用
void buildSpf(vector<int>& spf) {
    spf.resize(MAXB + 1);
    for (int i = 0; i <= MAXB; i++) {
        spf[i] = i;
    }
    for (int i = 2; i * 1LL * i <= MAXB; i++) {
        if (spf[i] == i) {
            for (int j = i * i; j <= MAXB; j += i) {
                if (spf[j] == j) {
                    spf[j] = i;
                }
            }
        }
    }
}

long long countPairs(const vector<int>& vals) {
    vector<int> spf;
    buildSpf(spf);
    long long cnt1 = 0;
    long long special = 0;
    map<int, long long> primeCnt;
    map<int, long long> squareCnt;
    for (size_t idx = 0; idx < vals.size(); idx++) {
        int x = vals[idx];
        if (x == 1) {
            // 1 只能和 p^3 或 p*q 配对
            cnt1++;
            continue;
        }
        int n = x;
        vector<pair<int, int> > factors;
        while (n > 1) {
            int p = spf[n];
            int c = 0;
            while (n % p == 0) {
                n /= p;
                c++;
            }
            factors.push_back(make_pair(p, c));
        }
        if ((int)factors.size() == 1) {
            int p = factors[0].first;
            int c = factors[0].second;
            if (c == 1) {
                primeCnt[p]++;
            } else if (c == 2) {
                squareCnt[p]++;
            } else if (c == 3) {
                special++;
            }
        } else if ((int)factors.size() == 2 && factors[0].second == 1 && factors[1].second == 1) {
            // 两个不同质数之积
            special++;
        }
    }
    // 1 与「恰好四因子」的数
    long long ans = cnt1 * special;
    long long totalP = 0;
    for (map<int, long long>::iterator it = primeCnt.begin(); it != primeCnt.end(); ++it) {
        long long c = it->second;
        totalP += c;
        // 同一个质数两次乘起来是平方，因子个数不是 4
        ans -= c * (c - 1) / 2;
        map<int, long long>::iterator sq = squareCnt.find(it->first);
        if (sq != squareCnt.end()) {
            // p 与 p^2 乘积是 p^3
            ans += c * sq->second;
        }
    }
    // 不同质数两两配对
    ans += totalP * (totalP - 1) / 2;
    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(0);

    // 一行：先 m 再跟 m 个指纹
    int m;
    cin >> m;
    vector<int> vals(m);
    for (int i = 0; i < m; i++) {
        cin >> vals[i];
    }
    cout << countPairs(vals) << "\n";
    return 0;
}
