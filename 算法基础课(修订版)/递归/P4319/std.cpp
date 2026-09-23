#include <bits/stdc++.h>
using namespace std;

// 抽象基类：表达式节点
struct Node {
    virtual unordered_map<string,int> calc() = 0;
    virtual ~Node() = default;
};

// 普通关键词节点
struct TokenNode : Node {
    string tok;
    TokenNode(const string& s) : tok(s) {}
    unordered_map<string,int> calc() override {
        return {{tok, 1}};
    }
};

// 顺序节点：依次执行多个子节点
struct SequenceNode : Node {
    vector<Node*> children;
    unordered_map<string,int> calc() override {
        unordered_map<string,int> res;
        for (auto* c : children) {
            auto m = c->calc();
            for (auto& [k,v] : m) {
                res[k] += v;
            }
        }
        return res;
    }
    ~SequenceNode() { for (auto* c: children) delete c; }
};

// 分支节点：必选或可选
struct BranchNode : Node {
    vector<Node*> options;
    bool required; // true 表示 { … }，false 表示 [ … ]
    unordered_map<string,int> calc() override {
        vector<unordered_map<string,int>> ms;
        for (auto* opt : options)
            ms.push_back(opt->calc());
        if (!required) {
            // 可选：加入一个空分支
            ms.push_back({});
        }
        // 对所有分支取关键词最小值
        unordered_map<string,int> res;
        // 收集所有关键词
        set<string> keys;
        for (auto& m: ms)
            for (auto& [k,_]: m)
                keys.insert(k);
        for (auto& k: keys) {
            int mn = INT_MAX;
            for (auto& m: ms) {
                mn = min(mn, m.count(k) ? m[k] : 0);
            }
            if (mn>0) res[k] = mn;
        }
        return res;
    }
    ~BranchNode() { for (auto* c: options) delete c; }
};

// 全局变量：令牌列表及指针
vector<string> T;
int pos = 0;

// 解析一个节点（可能是序列或单一）
Node* parseNode();

// 解析分支 { … } 或 [ … ]
BranchNode* parseBranch() {
    bool req = (T[pos] == "{");
    pos++; // 跳过 { 或 [
    BranchNode* bn = new BranchNode();
    bn->required = req;
    // 分支内部其实是若干选项，以 '|' 分隔
    while (pos < T.size() && (req ? T[pos]!="}" : T[pos]!="]")) {
        // 解析一个选项序列
        SequenceNode* seq = new SequenceNode();
        while (pos < T.size() && T[pos]!="|" && T[pos]!=(req? "}" : "]")) {
            if (T[pos]=="{" || T[pos]=="[") {
                seq->children.push_back(parseBranch());
            } else {
                seq->children.push_back(new TokenNode(T[pos]));
                pos++;
            }
        }
        bn->options.push_back(seq);
        if (T[pos] == "|") pos++;
    }
    pos++; // 跳过 } 或 ]
    return bn;
}

// 解析整个表达式为序列节点
Node* parseNode() {
    SequenceNode* seq = new SequenceNode();
    while (pos < T.size()) {
        if (T[pos] == "{" || T[pos] == "[") {
            seq->children.push_back(parseBranch());
        } else if (T[pos] == "}" || T[pos] == "]" || T[pos] == "|") {
            break;
        } else {
            seq->children.push_back(new TokenNode(T[pos]));
            pos++;
        }
    }
    return seq;
}

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    // 读入整行并分词
    string line;
    getline(cin, line);
    istringstream iss(line);
    string w;
    while (iss >> w) T.push_back(w);

    // 构建语法树
    Node* root = parseNode();
    // 计算最小出现次数映射
    auto mp = root->calc();
    delete root;

    // 只保留出现次数 ≥1 的关键词
    vector<pair<string,int>> ans;
    for (auto& [k,v]: mp) if (v>0) ans.emplace_back(k,v);
    sort(ans.begin(), ans.end(),
         [](auto& a, auto& b){ return a.first < b.first; });

    // 输出
    for (int i = 0; i < ans.size(); i++) {
        if (i) cout << ' ';
        cout << ans[i].first;
    }
    cout << "\n";
    for (int i = 0; i < ans.size(); i++) {
        if (i) cout << ' ';
        cout << ans[i].second;
    }
    cout << "\n";
    return 0;
}
