#include <bits/stdc++.h>
using namespace std;

int parent[1005];  // 并查集数组，用于存储每个联系人的父节点
int visited[1005]; // 记录某个联系人组是否已经处理过
struct Contact {
    int id;              // 联系人编号
    string name;         // 联系人姓名
    set<string> phones;  // 电话号码集合
} contacts[1005], mergedContacts[1005];
int mergedCount = 0;    // 合并后的联系人数量

// 并查集的查找操作，查找 x 的根节点
int findParent(int x) {
    if (parent[x] == x) return x;
    return parent[x] = findParent(parent[x]);  // 路径压缩优化
}

// 并查集的合并操作，将 x 和 y 所在的组合并
void unionGroups(int x, int y) {
    int rootX = findParent(x);
    int rootY = findParent(y);
    if (rootX != rootY) {
        parent[rootX] = rootY;  // 将 x 所在的组的根节点指向 y 所在组的根节点
    }
}

// 比较函数，用于对联系人进行排序
bool compareContacts(Contact a, Contact b) {
    if (a.name != b.name) return a.name < b.name;
    string minPhoneA = *(a.phones.begin());
    string minPhoneB = *(b.phones.begin());
    return minPhoneA < minPhoneB;
}

int main() {
    int n;  // 联系人数
    cin >> n;

    // 初始化并查集，每个联系人初始时自己是自己的父节点
    for (int i = 1; i <= n; i++) {
        parent[i] = i;
    }

    string inputLine;
    getline(cin, inputLine);  // 吃掉换行符
    for (int i = 1; i <= n; i++) {
        getline(cin, inputLine);
        int length = inputLine.length();

        Contact contact = {};  // 新建一个联系人
        int wordCount = 0;
        string word = "";

        // 解析输入，将姓名和电话号码分割存储
        for (int j = 0; j < length; j++) {
            word += inputLine[j];
            if (j == length - 1 || inputLine[j + 1] == ' ') {
                if (wordCount == 0) {
                    contact.name = word;  // 第一个单词为姓名
                } else {
                    contact.phones.insert(word);  // 后续的为电话号码
                }
                wordCount++;
                word = "";
                j++;  // 跳过空格
            }
        }

        contacts[i] = contact;  // 存储联系人信息

        // 合并当前联系人与前面所有联系人，检查是否有相同的电话号码
        for (int j = 1; j < i; j++) {
            for (const string &phoneJ : contacts[j].phones) {
                for (const string &phoneI : contact.phones) {
                    if (phoneJ == phoneI) {
                        unionGroups(j, i);  // 如果有相同号码则合并
                    }
                }
            }
        }
    }

    // 将联系人进行合并
    for (int i = 1; i <= n; i++) {
        int root = findParent(i);  // 找到联系人所在的组
        if (visited[root] == 0) {
            mergedContacts[++mergedCount] = contacts[i];  // 新组加入联系人
            visited[root] = mergedCount;  // 标记该组已处理
        } else {
            // 如果该组已存在联系人，则合并信息
            if (contacts[i].name < mergedContacts[visited[root]].name) {
                mergedContacts[visited[root]].name = contacts[i].name;  // 更新为字典序较小的姓名
            }
            // 合并电话号码
            for (const string &phone : contacts[i].phones) {
                mergedContacts[visited[root]].phones.insert(phone);
            }
        }
    }

    // 按规则排序联系人
    sort(mergedContacts + 1, mergedContacts + mergedCount + 1, compareContacts);

    // 输出结果
    for (int i = 1; i <= mergedCount; i++) {
        cout << mergedContacts[i].name << ' ';
        for (const string &phone : mergedContacts[i].phones) {
            cout << phone << ' ';
        }
        cout << '\n';
    }

    return 0;
}
