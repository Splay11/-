#include <iostream>
#include <vector>
using namespace std;

struct Node {
    int val;
    Node* prev;
    Node* next;
    Node(int v) : val(v), prev(nullptr), next(nullptr) {}
};

// 按输入顺序建双向循环链表；空序列返回空指针，对应原链表为空
Node* buildCircular(const vector<int>& vals) {
    if (vals.empty()) {
        return nullptr;
    }
    Node* head = new Node(vals[0]);
    Node* cur = head;
    // 依次把后续节点接到当前尾巴后面，同时维护 prev
    for (int i = 1; i < (int)vals.size(); i++) {
        Node* nxt = new Node(vals[i]);
        cur->next = nxt;
        nxt->prev = cur;
        cur = nxt;
    }
    // 头尾互连成环
    cur->next = head;
    head->prev = cur;
    return head;
}

// 把头插节点接到循环链表最前面；空表时新节点自环
Node* insertFront(Node* head, int x) {
    Node* nxt = new Node(x);
    if (head == nullptr) {
        // 空表：唯一节点的前驱、后继都指向自己
        nxt->next = nxt;
        nxt->prev = nxt;
        return nxt;
    }
    // 非空：新节点夹在原尾和原头之间，四条指针都要改
    Node* tail = head->prev;
    nxt->next = head;
    nxt->prev = tail;
    tail->next = nxt;
    head->prev = nxt;
    return nxt;
}

// 从新头沿后继走 cnt 步，正好一圈
vector<int> traverse(Node* head, int cnt) {
    vector<int> out;
    Node* cur = head;
    for (int i = 0; i < cnt; i++) {
        out.push_back(cur->val);
        cur = cur->next;
    }
    return out;
}

vector<int> insertAndList(const vector<int>& vals, int x) {
    Node* head = buildCircular(vals);
    head = insertFront(head, x);
    return traverse(head, (int)vals.size() + 1);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, x;
    cin >> n >> x;
    // n=0 时 vals 为空，不会读第二行
    vector<int> vals(n);
    for (int i = 0; i < n; i++) {
        cin >> vals[i];
    }
    vector<int> ans = insertAndList(vals, x);
    for (int i = 0; i < (int)ans.size(); i++) {
        if (i) {
            cout << ' ';
        }
        cout << ans[i];
    }
    cout << '\n';
    return 0;
}
