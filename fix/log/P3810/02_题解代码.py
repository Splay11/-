## 解题思路

给定五个仅含 `0~9` 的字符串 $a,b,c,d,e$。在所有进制 $x\in[2,10]$ 中，只有当五个串的每一位数字都小于 $x$ 时，称 $x$ 为“合法选择”。若在同一进制 $x$ 下满足

$$
A+B=C
$$

（按进制 $x$ 做加法，值用十进制表示），则把此时按进制 $x$ 解释出的 $D$ 与 $E$ 的十进制值相加，记为 $S_x=D+E$。
如果所有满足条件的 $x$ 的 $S_x$ 完全一致，输出该唯一值，否则输出 `"baka"`。若不存在任何满足条件的 $x$，也输出 `"baka"`。

算法要点（枚举进制）：

1. 预处理五个串的最大数字 `mx`，合法进制的下界是 `max(2, mx+1)`。
2. 对每个候选进制 $x$：

   * 把五个串用“**进制转十进制**”的方式解析（逐位 `val = val * x + digit`）。
   * 校验 $A+B=C$，若成立则计算 $S_x=D+E$。
   * 用一个变量记录首次出现的和值 `ans`，之后若遇到不同的和值则判定为不唯一。
3. 扫描结束：

   * 若至少有一个进制通过且所有和值相同，则输出 `ans`；否则输出 `"baka"`。


## 复杂度分析

设单个字符串长度不超过 9。

* 时间复杂度：对每组数据至多枚举 9 个进制、解析 5 个串，复杂度 $O(9 \times 5 \times \text{len})=O(\text{len})$，常数极小。
* 空间复杂度：仅用到若干整型变量，$O(1)$。

## 代码实现

### Python

```python
import sys

# 将仅含数字字符的字符串按进制 x 转为十进制，若遇到非法位返回 None
def parse_in_base(s, x):
    v = 0
    for ch in s:
        d = ord(ch) - ord('0')
        if d >= x:
            return None
        v = v * x + d
    return v

# 求解一组数据
def solve_case(a, b, c, d, e):
    # 计算五个串中的最大数字，用于缩小进制枚举范围
    mx_digit = max(max(ord(ch) - 48 for ch in s) for s in (a, b, c, d, e))
    start_base = max(2, mx_digit + 1)

    ans = None
    ok = False
    for x in range(start_base, 11):  # 只需从可能的最小进制开始到10
        A = parse_in_base(a, x)
        B = parse_in_base(b, x)
        C = parse_in_base(c, x)
        if A is None or B is None or C is None:
            continue
        if A + B == C:
            D = parse_in_base(d, x)
            E = parse_in_base(e, x)
            if D is None or E is None:
                continue
            S = D + E
            if not ok:
                ans = S
                ok = True
            elif S != ans:
                return "baka"
    return str(ans) if ok else "baka"

def main():
    data = sys.stdin.read().strip().split()
    it = iter(data)
    t = int(next(it))
    out = []
    for _ in range(t):
        a = next(it); b = next(it); c = next(it); d = next(it); e = next(it)
        out.append(solve_case(a, b, c, d, e))
    print("\n".join(out))

if __name__ == "__main__":
    main()
```

### Java

```java
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.util.StringTokenizer;

public class Main {

    // 把十进制字符组成的串按进制 x 解析为十进制；若含非法位返回 -1
    static long parseInBase(String s, int x) {
        long v = 0L;
        for (int i = 0; i < s.length(); i++) {
            int d = s.charAt(i) - '0';
            if (d >= x) return -1L;      // 非法位
            v = v * x + d;
        }
        return v;
    }

    // 求解一组数据
    static String solveCase(String a, String b, String c, String d, String e) {
        // 求五个串的最大数字，得到最小可能进制
        int mxDigit = 0;
        String[] arr = {a, b, c, d, e};
        for (String s : arr) {
            for (int i = 0; i < s.length(); i++) {
                mxDigit = Math.max(mxDigit, s.charAt(i) - '0');
            }
        }
        int startBase = Math.max(2, mxDigit + 1);

        boolean ok = false;
        long ans = -1;

        for (int x = startBase; x <= 10; x++) {
            long A = parseInBase(a, x);
            long B = parseInBase(b, x);
            long C = parseInBase(c, x);
            if (A < 0 || B < 0 || C < 0) continue;
            if (A + B == C) {
                long D = parseInBase(d, x);
                long E = parseInBase(e, x);
                if (D < 0 || E < 0) continue; // 理论上不会发生
                long S = D + E;
                if (!ok) {
                    ans = S;
                    ok = true;
                } else if (S != ans) {
                    return "baka";
                }
            }
        }
        return ok ? String.valueOf(ans) : "baka";
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        // 读入测试组数
        int t = Integer.parseInt(br.readLine().trim());
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < t; i++) {
            // 每组数据同一行包含五个字符串，用空格分隔
            StringTokenizer st = new StringTokenizer(br.readLine());
            String a = st.nextToken();
            String b = st.nextToken();
            String c = st.nextToken();
            String d = st.nextToken();
            String e = st.nextToken();
            sb.append(solveCase(a, b, c, d, e)).append('\n');
        }
        System.out.print(sb.toString());
    }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

// 把仅含数字的字符串按进制 x 解析为十进制；若含非法位返回 -1
long long parse_in_base(const string& s, int x) {
    long long v = 0;
    for (char ch : s) {
        int d = ch - '0';
        if (d >= x) return -1;   // 非法位
        v = v * x + d;
    }
    return v;
}

// 求解一组数据
string solve_case(const string& a, const string& b, const string& c,
                  const string& d, const string& e) {
    int mxDigit = 0;
    for (char ch : a) mxDigit = max(mxDigit, ch - '0');
    for (char ch : b) mxDigit = max(mxDigit, ch - '0');
    for (char ch : c) mxDigit = max(mxDigit, ch - '0');
    for (char ch : d) mxDigit = max(mxDigit, ch - '0');
    for (char ch : e) mxDigit = max(mxDigit, ch - '0');
    int startBase = max(2, mxDigit + 1);

    bool ok = false;
    long long ans = -1;

    for (int x = startBase; x <= 10; ++x) {
        long long A = parse_in_base(a, x);
        long long B = parse_in_base(b, x);
        long long C = parse_in_base(c, x);
        if (A < 0 || B < 0 || C < 0) continue;
        if (A + B == C) {
            long long D = parse_in_base(d, x);
            long long E = parse_in_base(e, x);
            if (D < 0 || E < 0) continue;
            long long S = D + E;
            if (!ok) {
                ans = S;
                ok = true;
            } else if (S != ans) {
                return "baka";
            }
        }
    }
    return ok ? to_string(ans) : string("baka");
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int t;
    if (!(cin >> t)) return 0;
    while (t--) {
        string a, b, c, d, e;
        cin >> a >> b >> c >> d >> e; // 同一行或多行读均可
        cout << solve_case(a, b, c, d, e) << "\n";
    }
    return 0;
}
```