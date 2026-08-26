## 解题思路

一次变换从左到右扫描串 $z$：对位置 $p$，若当前字符 $c$ 在左侧出现次数等于右侧出现次数，则把该位改成下一个字母（`'z'`→`'a'`），修改立即生效。

直接模拟 $r$ 次：用字母频次数组维护，单次变换 $O(m)$。观察可知，过程要么很快稳定，要么进入周期为 $26$ 的循环；进入循环后，每个会变的位置每步恰好 $+1$（模 $26$）。

因此维护最近 $27$ 个串状态：一旦发现当前串与 $26$ 步前相同，即可对“每步会变”的位置一次性加上剩余次数对 $26$ 取模，跳过后续模拟。

## 复杂度分析

单次变换 $O(m)$。进入周期前的步数在本题数据下很小，总体可接受；跳转后为 $O(m)$。全体 $m$、$r$ 之和均不超过 $10^5$。

## 代码实现

### Python

```python
from array import array

def solve_one(z, r):
    a = array("b", (ord(ch) - 97 for ch in z))  # 串 z 转 0..25
    n = len(a)
    done = 0
    hist = []  # 最近至多 26 步的 (哈希, 快照)
    while done < r:
        h = hash(a.tobytes())
        if len(hist) >= 26 and h == hist[-26][0] and hist[-26][1] == a.tobytes():
            # 已进入周期 26：找出会变的位置并跳转
            rem = r - done
            b = array("b", a)
            freq = [0] * 26
            for i in range(n):
                freq[b[i]] += 1
            left = [0] * 26
            ch = []
            for i in range(n):
                c = b[i]
                if left[c] == freq[c] - left[c] - 1:
                    freq[c] -= 1
                    nc = c + 1 if c < 25 else 0
                    b[i] = nc
                    freq[nc] += 1
                    left[nc] += 1
                    ch.append(i)
                else:
                    left[c] += 1
            add = rem % 26
            for i in ch:
                a[i] = (a[i] + add) % 26
            break
        hist.append((h, a.tobytes()))
        if len(hist) > 26:
            hist.pop(0)
        # 做一次变换
        freq = [0] * 26
        for i in range(n):
            freq[a[i]] += 1
        left = [0] * 26
        changed = False
        for i in range(n):
            c = a[i]
            if left[c] == freq[c] - left[c] - 1:
                freq[c] -= 1
                nc = c + 1 if c < 25 else 0
                a[i] = nc
                freq[nc] += 1
                left[nc] += 1
                changed = True
            else:
                left[c] += 1
        done += 1
        if not changed:
            break
    return "".join(chr(x + 97) for x in a)

q = int(input())
for _ in range(q):
    m, r = map(int, input().split())
    z = input().strip()
    print(solve_one(z, r))
```

### Java

```java
import java.io.*;
import java.util.*;

public class Main {
    // 对串做一次从左到右的平衡字母变换
    static String applyOnce(String s) {
        int n = s.length();
        char[] arr = s.toCharArray();
        int[] freq = new int[26], left = new int[26];
        for (char ch : arr) freq[ch - 'a']++;
        for (int i = 0; i < n; i++) {
            int c = arr[i] - 'a';
            if (left[c] == freq[c] - left[c] - 1) {
                freq[c]--;
                int nc = (c + 1) % 26;
                arr[i] = (char) ('a' + nc);
                freq[nc]++;
                left[nc]++;
            } else left[c]++;
        }
        return new String(arr);
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int q = Integer.parseInt(br.readLine().trim());
        StringBuilder out = new StringBuilder();
        while (q-- > 0) {
            StringTokenizer st = new StringTokenizer(br.readLine());
            int m = Integer.parseInt(st.nextToken());
            int r = Integer.parseInt(st.nextToken());
            String z = br.readLine().trim();
            ArrayDeque<String> window = new ArrayDeque<>();
            window.addLast(z);
            int done = 0;
            while (done < r) {
                String nxt = applyOnce(z);
                done++;
                if (nxt.equals(z)) break; // 已稳定
                z = nxt;
                window.addLast(z);
                if (window.size() > 27) window.removeFirst();
                if (window.size() == 27 && window.peekFirst().equals(window.peekLast())) {
                    // 周期 26：对会变位置加上剩余步数
                    int rem = r - done;
                    String s0 = window.peekFirst();
                    Iterator<String> it = window.iterator();
                    it.next();
                    String s1 = it.next();
                    int add = rem % 26;
                    char[] arr = z.toCharArray();
                    for (int i = 0; i < m; i++) {
                        if (s0.charAt(i) != s1.charAt(i)) {
                            arr[i] = (char) ('a' + (arr[i] - 'a' + add) % 26);
                        }
                    }
                    z = new String(arr);
                    break;
                }
            }
            out.append(z).append('\n');
        }
        System.out.print(out);
    }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

// 对串做一次从左到右的平衡字母变换
string apply_once(string s) {
    int n = (int)s.size();
    array<int, 26> freq{}, left{};
    for (char ch : s) ++freq[ch - 'a'];
    for (int i = 0; i < n; ++i) {
        int c = s[i] - 'a';
        if (left[c] == freq[c] - left[c] - 1) {
            --freq[c];
            int nc = (c + 1) % 26;
            s[i] = char('a' + nc);
            ++freq[nc];
            ++left[nc];
        } else ++left[c];
    }
    return s;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int q;
    cin >> q;
    while (q--) {
        int m, r;
        string z;
        cin >> m >> r >> z;
        deque<string> window;
        window.push_back(z);
        int done = 0;
        while (done < r) {
            string nxt = apply_once(z);
            ++done;
            if (nxt == z) break; // 已稳定
            z.swap(nxt);
            window.push_back(z);
            if ((int)window.size() > 27) window.pop_front();
            if ((int)window.size() == 27 && window.front() == window.back()) {
                // 周期 26：跳转剩余变换
                int rem = r - done;
                string s0 = window[0], s1 = window[1];
                int add = rem % 26;
                for (int i = 0; i < m; ++i)
                    if (s0[i] != s1[i])
                        z[i] = char('a' + (z[i] - 'a' + add) % 26);
                break;
            }
        }
        cout << z << '\n';
    }
    return 0;
}
```
