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

// 把长度为 n 的单链表向右旋转 k 位
Node* rotateRight(Node* head, int n, int k) {
    if (n == 0 || head == nullptr) {
        return nullptr;
    }
    k %= n;
    if (k == 0) {
        return head;
    }
    // 先走到尾并收成环，再数 n-k 步断开
    Node* tail = head;
    while (tail->next != nullptr) {
        tail = tail->next;
    }
    tail->next = head;
    int steps = n - k;
    Node* newTail = head;
    for (int i = 0; i < steps - 1; i++) {
        newTail = newTail->next;
    }
    Node* newHead = newTail->next;
    newTail->next = nullptr;
    return newHead;
}

vector<int> toList(Node* head) {
    vector<int> out;
    for (Node* cur = head; cur != nullptr; cur = cur->next) {
        out.push_back(cur->val);
    }
    return out;
}

vector<int> rotateVals(const vector<int>& vals, int k) {
    Node* head = buildList(vals);
    head = rotateRight(head, (int)vals.size(), k);
    return toList(head);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    long long k;
    cin >> n >> k;
    if (n == 0) {
        // 空链表输出空行
        cout << '\n';
        return 0;
    }
    vector<int> vals(n);
    for (int i = 0; i < n; i++) {
        cin >> vals[i];
    }
    // k 最大 2e9，先对 n 取模再旋转
    int kk = (int)(k % n);
    vector<int> ans = rotateVals(vals, kk);
    for (int i = 0; i < (int)ans.size(); i++) {
        if (i) {
            cout << ' ';
        }
        cout << ans[i];
    }
    cout << '\n';
    return 0;
}
