#include <bits/stdc++.h>
using namespace std;

struct ListNode {
    long long val;
    ListNode* next;
    ListNode(long long x) : val(x), next(nullptr) {}
};

#include "foo.cc"

static vector<long long> parseNumbers(const string& s) {
    vector<long long> nums;
    int n = (int)s.size();
    for (int i = 0; i < n; ) {
        if (s[i] == '-' || isdigit((unsigned char)s[i])) {
            int sign = 1;
            if (s[i] == '-') {
                sign = -1;
                i++;
            }
            long long x = 0;
            while (i < n && isdigit((unsigned char)s[i])) {
                x = x * 10 + (s[i] - '0');
                i++;
            }
            nums.push_back(x * sign);
        } else {
            i++;
        }
    }
    return nums;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string line, part;
    while (getline(cin, part)) line += part;

    vector<long long> nums = parseNumbers(line);

    ListNode dummy(0);
    ListNode* tail = &dummy;
    for (long long x : nums) {
        tail->next = new ListNode(x);
        tail = tail->next;
    }

    Solution solution;
    cout << "\""+ solution.gameResult(dummy.next) + "\"";
    return 0;
}
