#include <iostream>
#include <queue>
#include <sstream>
#include <string>
#include <vector>
using namespace std;

struct Ver {
    int a, b, c;
};

bool operator<(const Ver& x, const Ver& y) {
    if (x.a != y.a) {
        return x.a < y.a;
    }
    if (x.b != y.b) {
        return x.b < y.b;
    }
    return x.c < y.c;
}

bool operator>(const Ver& x, const Ver& y) {
    return y < x;
}

bool operator<=(const Ver& x, const Ver& y) {
    return !(y < x);
}

bool operator>=(const Ver& x, const Ver& y) {
    return !(x < y);
}

Ver parse_ver(const string& s) {
    // 把 a.b.c 拆成三个整数
    Ver v;
    int pos1 = (int)s.find('.');
    int pos2 = (int)s.find('.', pos1 + 1);
    v.a = stoi(s.substr(0, pos1));
    v.b = stoi(s.substr(pos1 + 1, pos2 - pos1 - 1));
    v.c = stoi(s.substr(pos2 + 1));
    return v;
}

struct Dep {
    int pid;
    string op;
    Ver bound;
    bool has_op;
};

Dep parse_dep(const string& token) {
    // 先匹配两位运算符，避免把 >= 拆成 >
    string ops[4] = {">=", "<=", ">", "<"};
    Dep d;
    d.has_op = false;
    d.op = "";
    for (int i = 0; i < 4; i++) {
        size_t pos = token.find(ops[i]);
        if (pos != string::npos) {
            d.pid = stoi(token.substr(0, pos));
            d.op = ops[i];
            d.bound = parse_ver(token.substr(pos + ops[i].size()));
            d.has_op = true;
            return d;
        }
    }
    d.pid = stoi(token);
    return d;
}

bool version_ok(const Ver& actual, const Dep& d) {
    if (!d.has_op) {
        return true;
    }
    if (d.op == ">=") {
        return actual >= d.bound;
    }
    if (d.op == "<=") {
        return actual <= d.bound;
    }
    if (d.op == ">") {
        return actual > d.bound;
    }
    return actual < d.bound;
}

string install_order(int m, const vector<int>& pids, const vector<Ver>& vers,
                     const vector<vector<string> >& deps) {
    vector<Ver> ver_of(m);
    vector<vector<string> > dep_of(m);
    for (int i = 0; i < m; i++) {
        ver_of[pids[i]] = vers[i];
        dep_of[pids[i]] = deps[i];
    }

    // 先检查全部版本约束，有冲突直接 -1
    for (int pid = 0; pid < m; pid++) {
        for (int j = 0; j < (int)dep_of[pid].size(); j++) {
            Dep d = parse_dep(dep_of[pid][j]);
            if (!version_ok(ver_of[d.pid], d)) {
                return "-1";
            }
        }
    }

    // 边从被依赖者指向依赖者：先安装被依赖者
    vector<vector<int> > g(m);
    vector<int> indeg(m, 0);
    for (int pid = 0; pid < m; pid++) {
        for (int j = 0; j < (int)dep_of[pid].size(); j++) {
            Dep d = parse_dep(dep_of[pid][j]);
            g[d.pid].push_back(pid);
            indeg[pid]++;
        }
    }

    // 小根堆保证每次取出当前可安装编号最小的包
    priority_queue<int, vector<int>, greater<int> > heap;
    for (int i = 0; i < m; i++) {
        if (indeg[i] == 0) {
            heap.push(i);
        }
    }
    vector<int> order;
    while (!heap.empty()) {
        int u = heap.top();
        heap.pop();
        order.push_back(u);
        for (int k = 0; k < (int)g[u].size(); k++) {
            int v = g[u][k];
            indeg[v]--;
            if (indeg[v] == 0) {
                heap.push(v);
            }
        }
    }
    // 没能装完说明有环（含自己依赖自己）
    if ((int)order.size() != m) {
        return "-2";
    }
    string ans = "";
    for (int i = 0; i < m; i++) {
        if (i) {
            ans += " ";
        }
        ans += to_string(order[i]);
    }
    return ans;
}

int main() {
    int m;
    cin >> m;
    string line;
    getline(cin, line);
    vector<int> pids(m);
    vector<Ver> vers(m);
    vector<vector<string> > deps(m);
    for (int i = 0; i < m; i++) {
        getline(cin, line);
        stringstream ss(line);
        ss >> pids[i];
        string ver_s;
        ss >> ver_s;
        vers[i] = parse_ver(ver_s);
        string tok;
        while (ss >> tok) {
            deps[i].push_back(tok);
        }
    }
    cout << install_order(m, pids, vers, deps) << endl;
    return 0;
}
