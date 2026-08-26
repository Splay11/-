### 题面描述

题目给定一个游戏，共进行 $n$ 轮操作。每一轮操作中可以选择以下三种之一：

1. **插入操作**：在黑板上写入一个整数 $x$；
2. **删除操作**：擦去黑板上一个整数 $x$（题目保证该整数在黑板中一定存在）；
3. **询问操作**：查询黑板上哪个数字与给定整数 $x$ 的异或值最大。如果黑板为空，则输出 $-1$。

题目保证至少存在一次询问操作。

---

### 思路

由于操作数最多可达 $2 \times 10^5$，且每个数字 $x$ 的范围为 $1 \leq x \leq 10^9$，直接遍历黑板上所有数字进行计算会超时。因此，需要利用高效的数据结构——**字典树（Trie）** 来存储黑板上的数字，从而在 $O(31)$ 的时间内完成每次操作（因为 $10^9$ 的二进制表示最多约 $31$ 位）。

- **构造字典树**  
  对于每个数字 $x$，将其二进制表示（固定为 $31$ 位或 $32$ 位）从最高位到最低位依次插入字典树的对应路径。  
  每个节点维护两个分支（分别表示 $0$ 和 $1$）以及一个计数器，用以记录经过该节点的数字个数，这有助于处理重复数字以及在删除时准确更新节点信息。

- **插入操作**  
  当进行插入操作时，将数字 $x$ 按位插入字典树，每经过一个节点就将该节点的计数器加 $1$。

- **删除操作**  
  删除操作时同样沿着数字 $x$ 的二进制表示路径，经过的每个节点计数器减 $1$。题目保证删除时数字一定存在，因此不必担心不存在该路径的情况。

- **查询操作**  
  对于查询操作，给定一个整数 $x$，从字典树的根节点开始：
  - 从最高位到最低位，期望走与 $x$ 当前位互补的分支（即 $0$ 对应 $1$，$1$ 对应 $0$），因为不同的位异或结果为 $1$，从而使异或值更大。
  - 如果所期望的分支不存在或计数器为 $0$，则只能沿着与 $x$ 相同的分支继续。
  - 最终构造出的路径所对应的数字与 $x$ 的异或值即为最大值。
  - 如果黑板为空（即字典树根节点的计数器为 $0$），则输出 $-1$。

---
## cpp
```cpp
#include <iostream>
using namespace std;

// 固定二进制位数（这里选择 31 位，因为 10^9 < 2^31）
const int BITS = 31;

// 字典树节点结构体
struct TrieNode {
    int cnt;             // 经过该节点的数字个数（用于处理重复数字）
    TrieNode* child[2];  // 两个分支，child[0] 表示 0 分支，child[1] 表示 1 分支
    TrieNode() : cnt(0) {
        child[0] = child[1] = nullptr;
    }
};

// 插入数字 x 到字典树中
void insert(TrieNode* root, int x) {
    TrieNode* node = root;
    node->cnt++;  // 更新根节点计数
    // 从最高位（BITS位）到最低位遍历
    for (int i = BITS; i >= 0; i--) {
        int bit = (x >> i) & 1;  // 取 x 的第 i 位（二进制）
        if (!node->child[bit]) { // 若对应分支不存在，则创建新节点
            node->child[bit] = new TrieNode();
        }
        node = node->child[bit];
        node->cnt++;  // 经过该节点的数字数量加 1
    }
}

// 删除数字 x 从字典树中（题目保证 x 存在）
void remove(TrieNode* root, int x) {
    TrieNode* node = root;
    node->cnt--;  // 更新根节点计数
    for (int i = BITS; i >= 0; i--) {
        int bit = (x >> i) & 1;
        node = node->child[bit];
        node->cnt--;  // 经过该节点的数字数量减 1
    }
}

// 查询给定 x 与字典树中数字异或值的最大值
int query(TrieNode* root, int x) {
    // 如果字典树为空则返回 -1
    if (root->cnt == 0) return -1;
    TrieNode* node = root;
    int res = 0;  // 用于累加构造出的最大异或值
    // 从最高位到最低位查找最优路径
    for (int i = BITS; i >= 0; i--) {
        int bit = (x >> i) & 1;
        int opp = 1 - bit;  // 期望走与 x 当前位相反的分支
        // 如果相反分支存在且有数字经过，则走该分支，异或结果该位为 1
        if (node->child[opp] != nullptr && node->child[opp]->cnt > 0) {
            res |= (1 << i);  // 将第 i 位置 1
            node = node->child[opp];
        } else {
            // 否则只能走相同分支
            node = node->child[bit];
        }
    }
    return res;  // 返回最终构造出的最大异或值
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    
    int n;
    cin >> n;
    
    TrieNode* root = new TrieNode();
    while (n--) {
        int op, x;
        cin >> op >> x;
        if (op == 1) {           // 插入操作
            insert(root, x);
        } else if (op == 2) {    // 删除操作
            remove(root, x);
        } else if (op == 3) {    // 查询操作
            cout << query(root, x) << "\n";
        }
    }
    return 0;
}

```
## python
```python
# 定义字典树节点类
class TrieNode:
    def __init__(self):
        self.child = [None, None]  # 两个分支，分别代表 0 和 1
        self.cnt = 0               # 经过该节点的数字个数

# 插入数字 x 到字典树中
def insert(root, x):
    node = root
    node.cnt += 1
    # 固定使用 32 位（或 31 位，根据题目数字范围；这里用 32 位保证万无一失）
    for i in range(31, -1, -1):
        bit = (x >> i) & 1
        if node.child[bit] is None:
            node.child[bit] = TrieNode()
        node = node.child[bit]
        node.cnt += 1

# 删除数字 x 从字典树中（保证 x 存在）
def remove(root, x):
    node = root
    node.cnt -= 1
    for i in range(31, -1, -1):
        bit = (x >> i) & 1
        node = node.child[bit]
        node.cnt -= 1

# 查询给定 x 与字典树中数字异或值的最大值
def query(root, x):
    # 如果黑板（字典树）为空，则返回 -1
    if root.cnt == 0:
        return -1
    node = root
    res = 0
    for i in range(31, -1, -1):
        bit = (x >> i) & 1
        opp = 1 - bit  # 优先选择相反的位
        if node.child[opp] is not None and node.child[opp].cnt > 0:
            res |= (1 << i)
            node = node.child[opp]
        else:
            node = node.child[bit]
    return res

if __name__ == '__main__':
    import sys
    input = sys.stdin.readline
    n = int(input().strip())
    root = TrieNode()
    for _ in range(n):
        parts = input().split()
        op = int(parts[0])
        x = int(parts[1])
        if op == 1:
            insert(root, x)
        elif op == 2:
            remove(root, x)
        elif op == 3:
            print(query(root, x))

```
## java
```java
import java.util.Scanner;

// 定义字典树节点类
class TrieNode {
    int cnt;            // 经过该节点的数字个数
    TrieNode[] child;   // 两个分支，child[0] 表示 0 分支，child[1] 表示 1 分支

    public TrieNode() {
        cnt = 0;
        child = new TrieNode[2];
    }
}

public class Main {
    // 固定二进制位数，使用 31 位或 32 位（题目数据范围内使用 31 位即可）
    static final int BITS = 31;

    // 插入数字 x 到字典树中
    static void insert(TrieNode root, int x) {
        TrieNode node = root;
        node.cnt++;  // 更新根节点计数
        for (int i = BITS; i >= 0; i--) {
            int bit = (x >> i) & 1;
            if (node.child[bit] == null) {
                node.child[bit] = new TrieNode();
            }
            node = node.child[bit];
            node.cnt++;  // 经过该节点的数字数量加 1
        }
    }

    // 删除数字 x 从字典树中（保证 x 存在）
    static void remove(TrieNode root, int x) {
        TrieNode node = root;
        node.cnt--;  // 更新根节点计数
        for (int i = BITS; i >= 0; i--) {
            int bit = (x >> i) & 1;
            node = node.child[bit];
            node.cnt--;  // 经过该节点的数字数量减 1
        }
    }

    // 查询给定 x 与字典树中数字异或值的最大值
    static int query(TrieNode root, int x) {
        // 如果字典树为空，则返回 -1
        if (root.cnt == 0) return -1;
        TrieNode node = root;
        int res = 0;
        for (int i = BITS; i >= 0; i--) {
            int bit = (x >> i) & 1;
            int opp = 1 - bit;  // 希望走与 x 当前位相反的分支
            if (node.child[opp] != null && node.child[opp].cnt > 0) {
                res |= (1 << i);  // 将第 i 位置 1
                node = node.child[opp];
            } else {
                node = node.child[bit];
            }
        }
        return res;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        TrieNode root = new TrieNode();
        // 逐轮处理操作
        for (int i = 0; i < n; i++) {
            int op = sc.nextInt();
            int x = sc.nextInt();
            if (op == 1) {          // 插入操作
                insert(root, x);
            } else if (op == 2) {   // 删除操作
                remove(root, x);
            } else if (op == 3) {   // 查询操作
                System.out.println(query(root, x));
            }
        }
        sc.close();
    }
}

```