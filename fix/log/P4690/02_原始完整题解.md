## 解题思路

设当前整数为 $x$，每次操作后要输出 $x$ 的二进制中 $1$ 的个数。

如果每次真的去维护大整数，再重新统计二进制里 $1$ 的数量，那么在数据范围 $n \le 10^6$ 下显然不合适。
因此这里使用的核心算法是：用二进制的“连续段”来模拟，也就是维护二进制表示的运行长度编码（$RLE$）。

### 核心思路

把当前二进制表示按从高位到低位压成若干段，例如：

* $11000111$ 可以表示成：

  * $1$ 段长度为 $2$
  * $0$ 段长度为 $3$
  * $1$ 段长度为 $3$

同时维护当前二进制中 $1$ 的总个数 $cnt$。

这样四种操作都只会影响二进制末尾附近的若干段：

* `+`：相当于二进制加一
  只会处理末尾连续的 $1$ 和它前面的一个 $0$
* `-`：相当于二进制减一（但保证 $x \ge 0$）
  只会处理末尾连续的 $0$ 和它前面的一个 $1$
* `*`：乘以 $2$
  相当于末尾补一个 $0$
* `/`：除以 $2$ 向下取整
  相当于删掉最低位

因此每次操作只需要修改栈尾若干段，并同步维护 $cnt$ 即可。

### 实现方法

用两个栈数组维护：

* $bits[i]$：这一段是 $0$ 还是 $1$
* $lens[i]$：这一段的长度

再写一个辅助函数 `add(bit, len)`：

* 如果新加入的段和当前栈顶段的 bit 相同，就直接合并
* 否则新开一段

这样可以始终保证段数最少，代码也更简洁。

## 复杂度分析

设操作串长度为 $n$。

* 时间复杂度：$O(n)$
  每次操作只会修改栈尾常数个连续段，因此总复杂度为 $O(n)$。
* 空间复杂度：$O(n)$
  最坏情况下需要维护 $O(n)$ 个连续段。

这个复杂度可以满足 $n \le 10^6$ 的要求。

## 代码实现

### Python

```python
import sys


# 每一段用 [bit, len] 表示
# bit 表示这一段是 0 还是 1
# len 表示这一段长度

# 向末尾加入一段，若和栈顶相同则合并
def add_seg(st, bit, length):
    if length <= 0:
        return
    if st and st[-1][0] == bit:
        st[-1][1] += length
    else:
        st.append([bit, length])


# 删除末尾一位
def remove_last_bit(st):
    if not st:
        return
    st[-1][1] -= 1
    if st[-1][1] == 0:
        st.pop()


# 处理操作串
def solve_ops(s):
    st = []      # 二进制连续段
    cnt = 0      # 当前二进制中 1 的个数
    ans = []

    for ch in s:
        if ch == '+':
            if not st:
                # 0 + 1 = 1
                add_seg(st, 1, 1)
                cnt += 1
            elif st[-1][0] == 0:
                # 最低位是 0，直接改成 1
                remove_last_bit(st)
                add_seg(st, 1, 1)
                cnt += 1
            else:
                # 末尾若干个 1 进位
                k = st[-1][1]
                st.pop()
                cnt -= k

                if not st:
                    # 原来全是 1，例如 111 + 1 = 1000
                    add_seg(st, 1, 1)
                    cnt += 1
                    add_seg(st, 0, k)
                else:
                    # 前面一定是 0，把那个 0 变成 1，再补 k 个 0
                    remove_last_bit(st)
                    add_seg(st, 1, 1)
                    cnt += 1
                    add_seg(st, 0, k)

        elif ch == '-':
            if not st:
                # 0 不能再减
                pass
            elif st[-1][0] == 1:
                # 最低位是 1，直接减掉这一位
                remove_last_bit(st)
                cnt -= 1

                # 若结果还大于 0，则最低位补成 0
                if st:
                    add_seg(st, 0, 1)
            else:
                # 末尾若干个 0，需要借位
                k = st[-1][1]
                st.pop()

                # 前面一定有一段 1
                remove_last_bit(st)
                cnt -= 1

                # 若前面还有更高位，则这个借位后的 0 需要保留
                if st:
                    add_seg(st, 0, 1)

                # 后面 k 个 0 变成 k 个 1
                add_seg(st, 1, k)
                cnt += k

        elif ch == '*':
            # 乘 2，相当于末尾补 0；0 * 2 仍是 0
            if st:
                add_seg(st, 0, 1)

        else:  # ch == '/'
            # 除 2，相当于删最低位；0 / 2 仍是 0
            if st:
                if st[-1][0] == 1:
                    cnt -= 1
                remove_last_bit(st)

        ans.append(str(cnt))

    return ans


def main():
    input = sys.stdin.readline
    n = int(input().strip())
    s = input().strip()

    ans = solve_ops(s)
    sys.stdout.write('\n'.join(ans))


if __name__ == "__main__":
    main()

```

### Java

```java
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.ArrayList;

public class Main {

    // 每一段的信息
    static class Node {
        int bit; // 这一段是 0 还是 1
        int len; // 这一段长度

        Node(int bit, int len) {
            this.bit = bit;
            this.len = len;
        }
    }

    // 向末尾加入一段，若和栈顶相同则合并
    static void addSeg(ArrayList<Node> st, int bit, int len) {
        if (len <= 0) return;

        if (!st.isEmpty() && st.get(st.size() - 1).bit == bit) {
            st.get(st.size() - 1).len += len;
        } else {
            st.add(new Node(bit, len));
        }
    }

    // 删除末尾一位
    static void removeLastBit(ArrayList<Node> st) {
        if (st.isEmpty()) return;

        Node last = st.get(st.size() - 1);
        last.len--;
        if (last.len == 0) {
            st.remove(st.size() - 1);
        }
    }

    // 处理操作串
    static StringBuilder solveOps(String s) {
        ArrayList<Node> st = new ArrayList<>(); // 二进制连续段
        int cnt = 0;                            // 当前二进制中 1 的个数
        StringBuilder ans = new StringBuilder();

        for (int i = 0; i < s.length(); i++) {
            char ch = s.charAt(i);

            if (ch == '+') {
                if (st.isEmpty()) {
                    // 0 + 1 = 1
                    addSeg(st, 1, 1);
                    cnt++;
                } else if (st.get(st.size() - 1).bit == 0) {
                    // 最低位是 0，直接改成 1
                    removeLastBit(st);
                    addSeg(st, 1, 1);
                    cnt++;
                } else {
                    // 末尾若干个 1 进位
                    int k = st.get(st.size() - 1).len;
                    st.remove(st.size() - 1);
                    cnt -= k;

                    if (st.isEmpty()) {
                        // 原来全是 1，例如 111 + 1 = 1000
                        addSeg(st, 1, 1);
                        cnt++;
                        addSeg(st, 0, k);
                    } else {
                        // 前面一定是 0，把那个 0 变成 1，再补 k 个 0
                        removeLastBit(st);
                        addSeg(st, 1, 1);
                        cnt++;
                        addSeg(st, 0, k);
                    }
                }
            } else if (ch == '-') {
                if (st.isEmpty()) {
                    // 0 不能再减
                } else if (st.get(st.size() - 1).bit == 1) {
                    // 最低位是 1，直接减掉这一位
                    removeLastBit(st);
                    cnt--;

                    // 若结果还大于 0，则最低位补成 0
                    if (!st.isEmpty()) {
                        addSeg(st, 0, 1);
                    }
                } else {
                    // 末尾若干个 0，需要借位
                    int k = st.get(st.size() - 1).len;
                    st.remove(st.size() - 1);

                    // 前面一定有一段 1
                    removeLastBit(st);
                    cnt--;

                    // 若前面还有更高位，则这个借位后的 0 需要保留
                    if (!st.isEmpty()) {
                        addSeg(st, 0, 1);
                    }

                    // 后面 k 个 0 变成 k 个 1
                    addSeg(st, 1, k);
                    cnt += k;
                }
            } else if (ch == '*') {
                // 乘 2，相当于末尾补 0；0 * 2 仍是 0
                if (!st.isEmpty()) {
                    addSeg(st, 0, 1);
                }
            } else { // ch == '/'
                // 除 2，相当于删最低位；0 / 2 仍是 0
                if (!st.isEmpty()) {
                    if (st.get(st.size() - 1).bit == 1) {
                        cnt--;
                    }
                    removeLastBit(st);
                }
            }

            ans.append(cnt).append('\n');
        }

        return ans;
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        String s = br.readLine().trim();

        System.out.print(solveOps(s).toString());
    }
}

```

### C++

```cpp
#include <iostream>
#include <vector>
#include <string>
using namespace std;

struct Node {
    int bit;   // 这一段是 0 还是 1
    int len;   // 这一段长度
};

// 向末尾加入一段，若和栈顶相同则合并
void addSeg(vector<Node>& st, int bit, int len) {
    if (len <= 0) return;
    if (!st.empty() && st.back().bit == bit) {
        st.back().len += len;
    } else {
        st.push_back({bit, len});
    }
}

// 删除末尾一位
void removeLastBit(vector<Node>& st) {
    if (st.empty()) return;
    st.back().len--;
    if (st.back().len == 0) st.pop_back();
}

// 处理操作串
vector<int> solveOps(const string& s) {
    vector<Node> st;   // 二进制连续段
    int cnt = 0;       // 当前二进制中 1 的个数
    vector<int> ans;
    ans.reserve(s.size());

    for (char ch : s) {
        if (ch == '+') {
            if (st.empty()) {
                // 0 + 1 = 1
                addSeg(st, 1, 1);
                cnt++;
            } else if (st.back().bit == 0) {
                // 最低位是 0，直接改成 1
                removeLastBit(st);
                addSeg(st, 1, 1);
                cnt++;
            } else {
                // 末尾若干个 1 进位
                int k = st.back().len;
                st.pop_back();
                cnt -= k;

                if (st.empty()) {
                    // 原来全是 1，例如 111 + 1 = 1000
                    addSeg(st, 1, 1);
                    cnt++;
                    addSeg(st, 0, k);
                } else {
                    // 前面一定是 0，把那个 0 变成 1，再补 k 个 0
                    removeLastBit(st);
                    addSeg(st, 1, 1);
                    cnt++;
                    addSeg(st, 0, k);
                }
            }
        } else if (ch == '-') {
            if (st.empty()) {
                // 0 不能再减
            } else if (st.back().bit == 1) {
                // 最低位是 1，直接减掉这一位
                removeLastBit(st);
                cnt--;

                // 若结果还大于 0，则最低位补成 0
                if (!st.empty()) {
                    addSeg(st, 0, 1);
                }
            } else {
                // 末尾若干个 0，需要借位
                int k = st.back().len;
                st.pop_back();

                // 前面一定有一段 1
                removeLastBit(st);
                cnt--;

                // 若前面还有更高位，则这个借位后的 0 需要保留
                if (!st.empty()) {
                    addSeg(st, 0, 1);
                }

                // 后面 k 个 0 变成 k 个 1
                addSeg(st, 1, k);
                cnt += k;
            }
        } else if (ch == '*') {
            // 乘 2，相当于末尾补 0；0 * 2 仍是 0
            if (!st.empty()) {
                addSeg(st, 0, 1);
            }
        } else { // ch == '/'
            // 除 2，相当于删最低位；0 / 2 仍是 0
            if (!st.empty()) {
                if (st.back().bit == 1) cnt--;
                removeLastBit(st);
            }
        }

        ans.push_back(cnt);
    }

    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    string s;
    cin >> n >> s;

    vector<int> ans = solveOps(s);
    for (int x : ans) {
        cout << x << '\n';
    }

    return 0;
}

```