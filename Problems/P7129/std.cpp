#include <iostream>
#include <vector>
using namespace std;

struct Node {
    int val;
    Node* next;
    Node(int v) : val(v), next(nullptr) {}
};

// 把数组建成单链表，返回头节点
Node* buildList(const vector<int>& vals) {
    Node dummy(0);
    Node* cur = &dummy;
    for (int v : vals) {
        cur->next = new Node(v);
        cur = cur->next;
    }
    return dummy.next;
}

// 快指针先走 k 步，再和慢指针一起走，慢指针停在倒数第 k 个
int kthFromEnd(Node* head, int k) {
    Node* fast = head;
    for (int i = 0; i < k; i++) {
        fast = fast->next;
    }
    Node* slow = head;
    while (fast != nullptr) {
        fast = fast->next;
        slow = slow->next;
    }
    return slow->val;
}

int solve(const vector<int>& vals, int k) {
    Node* head = buildList(vals);
    return kthFromEnd(head, k);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, k;
    cin >> n >> k;
    vector<int> vals(n);
    for (int i = 0; i < n; i++) {
        cin >> vals[i];
    }
    cout << solve(vals, k) << '\n';
    return 0;
}
