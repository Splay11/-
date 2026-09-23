#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

struct Fenwick {
    int n;
    vector<int> c;
    Fenwick(int n_ = 0) { init(n_); }
    void init(int n_) {
        n = n_;
        c.assign(n + 1, 0);
    }
    void add(int i, int v) {
        // 在工位 i 上加上 v
        while (i <= n) {
            c[i] += v;
            i += i & -i;
        }
    }
    int pre(int i) {
        int s = 0;
        while (i > 0) {
            s += c[i];
            i -= i & -i;
        }
        return s;
    }
    int rng(int left, int right) {
        // 统计上游窗口 [left, right]
        if (left > right) {
            return 0;
        }
        return pre(right) - pre(left - 1);
    }
};

struct Station {
    long long w;
    int pos;
};

struct Query {
    long long thresh;
    int left;
    int right;
    int qid;
};

bool cmpStation(const Station& a, const Station& b) {
    return a.w < b.w;
}

bool cmpQuery(const Query& a, const Query& b) {
    return a.thresh < b.thresh;
}

vector<int> solve(int n, int d, long long k, const vector<long long>& w, const vector<int>& qs) {
    // 工位按重量、询问按阈值从小到大，离线插入树状数组
    int m = (int)qs.size();
    vector<Station> stations(n);
    for (int i = 1; i <= n; i++) {
        stations[i - 1].w = w[i];
        stations[i - 1].pos = i;
    }
    vector<Query> queries(m);
    for (int i = 0; i < m; i++) {
        int x = qs[i];
        int left = x - d;
        if (left < 1) {
            left = 1;
        }
        queries[i].thresh = w[x] - k;
        queries[i].left = left;
        queries[i].right = x - 1;
        queries[i].qid = i;
    }
    sort(stations.begin(), stations.end(), cmpStation);
    sort(queries.begin(), queries.end(), cmpQuery);
    Fenwick bit(n);
    vector<int> ans(m);
    int p = 0;
    for (int i = 0; i < m; i++) {
        while (p < n && stations[p].w <= queries[i].thresh) {
            bit.add(stations[p].pos, 1);
            p++;
        }
        ans[queries[i].qid] = bit.rng(queries[i].left, queries[i].right);
    }
    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(0);
    int n, m, d;
    long long k;
    cin >> n >> m >> d >> k;
    vector<long long> w(n + 1);
    for (int i = 1; i <= n; i++) {
        cin >> w[i];
    }
    vector<int> qs(m);
    for (int i = 0; i < m; i++) {
        cin >> qs[i];
    }
    vector<int> out = solve(n, d, k, w, qs);
    for (int i = 0; i < m; i++) {
        cout << out[i] << "\n";
    }
    return 0;
}
