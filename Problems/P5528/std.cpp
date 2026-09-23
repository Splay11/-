#include <bits/stdc++.h>
using namespace std;

struct Node {
    int key, value;
    long long expire;
    Node *prev, *next;
    Node(int k = 0, int v = 0, long long e = 0) : key(k), value(v), expire(e), prev(nullptr), next(nullptr) {}
};

class TTLLRU {
    int cap;
    unordered_map<int, Node*> mp;
    Node *head, *tail;  // 哨兵：head 后为最久未使用，tail 前为最近

    void remove(Node* x) {
        x->prev->next = x->next;
        x->next->prev = x->prev;
    }
    void addBack(Node* x) {
        x->prev = tail->prev;
        x->next = tail;
        tail->prev->next = x;
        tail->prev = x;
    }
    bool expired(Node* x, long long ts) const { return x->expire <= ts; }

    void evict(long long ts) {
        // 优先淘汰已过期
        for (Node* p = head->next; p != tail; p = p->next) {
            if (expired(p, ts)) {
                mp.erase(p->key);
                remove(p);
                delete p;
                return;
            }
        }
        // 否则淘汰 LRU
        Node* p = head->next;
        mp.erase(p->key);
        remove(p);
        delete p;
    }

public:
    TTLLRU(int c) : cap(c) {
        head = new Node();
        tail = new Node();
        head->next = tail;
        tail->prev = head;
    }
    void put(int key, int value, int ttl, long long ts) {
        long long exp = ts + ttl;
        if (mp.count(key)) {
            Node* x = mp[key];
            x->value = value;
            x->expire = exp;
            remove(x);
            addBack(x);
            return;
        }
        if ((int)mp.size() >= cap) evict(ts);
        Node* x = new Node(key, value, exp);
        mp[key] = x;
        addBack(x);
    }
    int get(int key, long long ts) {
        if (!mp.count(key)) return -1;
        Node* x = mp[key];
        if (expired(x, ts)) {
            mp.erase(key);
            remove(x);
            delete x;
            return -1;
        }
        remove(x);
        addBack(x);
        return x->value;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int capacity, q;
    cin >> capacity >> q;
    TTLLRU cache(capacity);
    for (int i = 0; i < q; ++i) {
        string op;
        cin >> op;
        if (op == "put") {
            int key, value, ttl;
            long long ts;
            cin >> key >> value >> ttl >> ts;
            cache.put(key, value, ttl, ts);
        } else {
            int key;
            long long ts;
            cin >> key >> ts;
            cout << cache.get(key, ts) << '\n';
        }
    }
    return 0;
}
