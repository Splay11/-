#include <iostream>
#include <string>
#include <vector>
using namespace std;

struct Node {
    Node* ch[26];
    bool end;
    Node() : end(false) {
        for (int i = 0; i < 26; i++) {
            ch[i] = nullptr;
        }
    }
};

// 把一个词根插入字典树
void insert(Node* root, const string& word) {
    Node* cur = root;
    for (int i = 0; i < (int)word.size(); i++) {
        int id = word[i] - 'a';
        if (cur->ch[id] == nullptr) {
            cur->ch[id] = new Node();
        }
        cur = cur->ch[id];
    }
    cur->end = true;
}

// 沿单词往下走，第一次碰到结束标记就是最短词根；否则整词保留
string shortestRoot(Node* root, const string& word) {
    Node* cur = root;
    for (int i = 0; i < (int)word.size(); i++) {
        int id = word[i] - 'a';
        if (cur->ch[id] == nullptr) {
            return word;
        }
        cur = cur->ch[id];
        if (cur->end) {
            return word.substr(0, i + 1);
        }
    }
    return word;
}

string solve(const vector<string>& dictionary, const string& sentence) {
    Node* root = new Node();
    for (int i = 0; i < (int)dictionary.size(); i++) {
        insert(root, dictionary[i]);
    }
    string ans;
    string word;
    // 按空格拆单词，边拆边替换
    for (int i = 0; i <= (int)sentence.size(); i++) {
        if (i == (int)sentence.size() || sentence[i] == ' ') {
            string rep = shortestRoot(root, word);
            if (!ans.empty()) {
                ans.push_back(' ');
            }
            ans += rep;
            word.clear();
        } else {
            word.push_back(sentence[i]);
        }
    }
    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<string> dictionary(n);
    for (int i = 0; i < n; i++) {
        cin >> dictionary[i];
    }
    string dummy;
    getline(cin, dummy);
    // 第三行是整句，可能很长
    string sentence;
    getline(cin, sentence);
    cout << solve(dictionary, sentence) << '\n';
    return 0;
}
