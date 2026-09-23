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

// 删除所有出现次数大于 1 的值
ListNode* deleteDuplicates(ListNode* head) {
    ListNode dummy(0, head);
    ListNode* pre = &dummy;
    while (pre->next) {
        ListNode* cur = pre->next;
        if (cur->next && cur->next->val == cur->val) {
            int x = cur->val;
            while (pre->next && pre->next->val == x) pre->next = pre->next->next;
        } else {
            pre = pre->next;
        }
    }
    return dummy.next;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    if (n == 0) {
        cout << '\n';
        return 0;
    }
    vector<int> vals(n);
    for (int i = 0; i < n; i++) cin >> vals[i];
    ListNode* head = deleteDuplicates(buildList(vals));
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
