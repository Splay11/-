#include <iostream>
#include <vector>
using namespace std;

struct ListNode {
    int val;
    ListNode* next;
    ListNode(int v = 0, ListNode* n = nullptr) : val(v), next(n) {}
};

ListNode* buildList(const vector<int>& vals) {
    ListNode dummy(0);
    ListNode* cur = &dummy;
    for (int v : vals) {
        cur->next = new ListNode(v);
        cur = cur->next;
    }
    return dummy.next;
}

// 反转区间 [left, right]（1-based），头插法
ListNode* reverseBetween(ListNode* head, int left, int right) {
    ListNode dummy(0, head);
    ListNode* pre = &dummy;
    for (int i = 0; i < left - 1; i++) pre = pre->next;
    ListNode* cur = pre->next;
    for (int i = 0; i < right - left; i++) {
        ListNode* nxt = cur->next;
        cur->next = nxt->next;
        nxt->next = pre->next;
        pre->next = nxt;
    }
    return dummy.next;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, left, right;
    cin >> n >> left >> right;
    vector<int> vals(n);
    for (int i = 0; i < n; i++) cin >> vals[i];
    ListNode* head = reverseBetween(buildList(vals), left, right);
    bool first = true;
    while (head) {
        if (!first) cout << ' ';
        first = false;
        cout << head->val;
        head = head->next;
    }
    cout << '\n';
    return 0;
}
