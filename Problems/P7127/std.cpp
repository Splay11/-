#include <iostream>
#include <vector>
using namespace std;

struct Node {
    int val;
    Node* prev;
    Node* next;
    Node(int v) : val(v), prev(nullptr), next(nullptr) {}
};

// 用给定序列建成双向循环链表，返回原头节点
Node* buildCircular(const vector<int>& vals) {
    Node* head = new Node(vals[0]);
    Node* cur = head;
    for (int i = 1; i < (int)vals.size(); i++) {
        Node* nxt = new Node(vals[i]);
        cur->next = nxt;
        nxt->prev = cur;
        cur = nxt;
    }
    // 头尾互连，形成循环
    cur->next = head;
    head->prev = cur;
    return head;
}

// 在循环链表最前面插入值为 x 的新节点，返回新头
Node* insertFront(Node* head, int x) {
    Node* nxt = new Node(x);
    Node* tail = head->prev;
    // 新节点夹在原来的尾和头之间
    nxt->next = head;
    nxt->prev = tail;
    tail->next = nxt;
    head->prev = nxt;
    return nxt;
}

// 从 head 沿后继走 cnt 步，收集节点值
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
