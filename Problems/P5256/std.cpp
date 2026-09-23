#include <algorithm>
#include <iostream>
#include <vector>
using namespace std;

struct Job {
    int s, e;
    long long v;
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<Job> jobs(n);
    for (int i = 0; i < n; ++i) {
        cin >> jobs[i].s >> jobs[i].e >> jobs[i].v;
    }
    sort(jobs.begin(), jobs.end(), [](const Job& a, const Job& b) {
        return a.e < b.e;
    });
    vector<int> ends(n);
    for (int i = 0; i < n; ++i) ends[i] = jobs[i].e;
    vector<long long> dp(n + 1, 0);
    for (int i = 1; i <= n; ++i) {
        int s = jobs[i - 1].s;
        long long v = jobs[i - 1].v;
        int k = (int)(upper_bound(ends.begin(), ends.begin() + (i - 1), s) - ends.begin());
        dp[i] = max(dp[i - 1], dp[k] + v);
    }
    cout << dp[n] << '\n';
    return 0;
}
