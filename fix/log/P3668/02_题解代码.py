## 解题思路

给出三个整数 $a,b,c$。我们可以选择其中**恰好一个**数乘上某个整数 $m$（$m$ 可为负、可为 0、也可为 1），然后允许对三个数任意重排。问能否得到一个等比数列。

**关键等价：** 三个数能重排成等比数列 $(x, y, z)$ 当且仅当

$$
y^2 = x \cdot z
$$

（允许公比为 0 或负数；例如 $(1,0,0)$ 的公比为 0。）

因此，只需考虑谁当“中项” $y$。又因为我们只允许把一个原数乘上 $m$，设被乘的数为 $x$，另外两个是 $y,z$。则有三种可能：

1. 把 $x\cdot m$ 放中间：
   $(x m)^2 = y z \Rightarrow m^2 = \dfrac{y z}{x^2}$。
   等价于：$y z$ 必须是 $x^2$ 的**非负完全平方倍**（特别地，若 $x=0$，则只需 $y z=0$，即 $y=0$ 或 $z=0$）。

2. 把 $y$ 放中间：
   $x m z = y^2 \Rightarrow m = \dfrac{y^2}{x z}$ 必须是整数。
   若 $x z=0$，则该式化为 $0=y^2$，即必须 $y=0$。

3. 把 $z$ 放中间：
   $x m y = z^2 \Rightarrow m = \dfrac{z^2}{x y}$ 必须是整数。
   若 $x y=0$，则该式化为 $0=z^2$，即必须 $z=0$。

对被乘元素分别取 $a$、$b$、$c$ 三种情况，逐一套用上面三条（总共常数次判断），若任意一种满足即可输出 YES，否则 NO。

## 复杂度分析

每组数据仅做常数次整数运算与整型开平方：

* 时间复杂度：$O(1)$ / 组
* 空间复杂度：$O(1)$

## 代码实现

### Python

```python
import sys
import math

def is_square_nonneg(x: int) -> bool:
    """判断x是否为非负完全平方"""
    if x < 0:
        return False
    r = int(math.isqrt(x))
    return r * r == x

def check_mul(x: int, y: int, z: int) -> bool:
    """选择把x乘以m，看是否可成等比（考虑三种中项位置）"""

    # 情况1：x*m为中项 -> (x*m)^2 = y*z
    if x == 0:
        # 左侧恒为0，需y*z==0
        if y == 0 or z == 0:
            return True
    else:
        q = y * z
        xx = x * x
        # 需 q = xx * (非负完全平方)
        if q % xx == 0:
            v = q // xx
            if is_square_nonneg(v):
                return True

    # 情况2：y为中项 -> x*m*z = y^2
    if x == 0 or z == 0:
        if y == 0:
            return True
    else:
        d = x * z
        y2 = y * y
        if y2 % d == 0:
            return True

    # 情况3：z为中项 -> x*m*y = z^2
    if x == 0 or y == 0:
        if z == 0:
            return True
    else:
        d = x * y
        z2 = z * z
        if z2 % d == 0:
            return True

    return False

def ok(a: int, b: int, c: int) -> bool:
    """三种被乘对象分别检查"""
    return check_mul(a, b, c) or check_mul(b, a, c) or check_mul(c, a, b)

def main():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    t = int(next(it))
    out = []
    for _ in range(t):
        a = int(next(it)); b = int(next(it)); c = int(next(it))
        out.append("YES" if ok(a, b, c) else "NO")
    print("\n".join(out))

if __name__ == "__main__":
    main()
```

### Java

```java
// 等比数列一次乘法判定
// 类名必须为 Main
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.util.StringTokenizer;

public class Main {
    static boolean isSquareNonneg(long x) {
        // 判断x是否为非负完全平方
        if (x < 0) return false;
        long r = (long)Math.sqrt((double)x); // 向下取整
        return r * r == x || (r + 1) * (r + 1) == x; // 双重保险
    }

    static boolean checkMul(long x, long y, long z) {
        // 情况1：x*m为中项 -> (x*m)^2 = y*z
        if (x == 0) {
            if (y == 0 || z == 0) return true;
        } else {
            long q = y * z;          // 乘积可能至1e18，使用long
            long xx = x * x;
            if (xx != 0 && q % xx == 0) {
                long v = q / xx;
                if (isSquareNonneg(v)) return true;
            }
        }

        // 情况2：y为中项 -> x*m*z = y^2
        if (x == 0 || z == 0) {
            if (y == 0) return true; // 0 = y^2 -> y必须为0
        } else {
            long d = x * z;
            long y2 = y * y;
            if (d != 0 && y2 % d == 0) return true;
        }

        // 情况3：z为中项 -> x*m*y = z^2
        if (x == 0 || y == 0) {
            if (z == 0) return true;
        } else {
            long d = x * y;
            long z2 = z * z;
            if (d != 0 && z2 % d == 0) return true;
        }

        return false;
    }

    static boolean ok(long a, long b, long c) {
        return checkMul(a, b, c) || checkMul(b, a, c) || checkMul(c, a, b);
    }

    public static void main(String[] args) throws IOException {
        // 使用BufferedReader + StringTokenizer读取
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringBuilder ans = new StringBuilder();
        StringTokenizer st;

        String s = br.readLine();
        while (s != null && s.trim().isEmpty()) s = br.readLine();
        int t = Integer.parseInt(s.trim());

        int cnt = 0;
        while (cnt < t) {
            String line = br.readLine();
            if (line == null) break;
            if (line.trim().isEmpty()) continue;
            st = new StringTokenizer(line);
            if (st.countTokens() < 3) {
                // 若一行不足三个数，继续读下一行补全
                String extra = br.readLine();
                if (extra == null) break;
                line = line + " " + extra;
                st = new StringTokenizer(line);
            }
            long a = Long.parseLong(st.nextToken());
            long b = Long.parseLong(st.nextToken());
            long c = Long.parseLong(st.nextToken());

            ans.append(ok(a, b, c) ? "YES" : "NO").append('\n');
            cnt++;
        }
        System.out.print(ans.toString());
    }
}
```

### C++

```cpp
// 等比数列一次乘法判定
#include <bits/stdc++.h>
using namespace std;

using int64 = long long;

// 判断x是否为非负完全平方
bool is_square_nonneg(int64 x) {
    if (x < 0) return false;
    int64 r = sqrt((long double) x);
    // 纠正可能的舍入误差
    while (r * r > x) --r;
    while ((r + 1) * (r + 1) <= x) ++r;
    return r * r == x;
}

// 选择把x乘以m，检查三种中项情况
bool check_mul(int64 x, int64 y, int64 z) {
    // 情况1：x*m为中项 -> (x*m)^2 = y*z
    if (x == 0) {
        if (y == 0 || z == 0) return true; // 0 = y*z
    } else {
        int64 q = y * z; 
        int64 xx = x * x;
        if (q % xx == 0) {
            int64 v = (q / xx);
            if (is_square_nonneg(v)) return true;
        }
    }

    // 情况2：y为中项 -> x*m*z = y^2
    if (x == 0 || z == 0) {
        if (y == 0) return true; // 0 = y^2
    } else {
        int64 d = x * z;
        int64 y2 = y * y;
        if (y2 % d == 0) return true;
    }

    // 情况3：z为中项 -> x*m*y = z^2
    if (x == 0 || y == 0) {
        if (z == 0) return true; // 0 = z^2
    } else {
        int64 d = x * y;
        int64 z2 = z * z;
        if (z2 % d == 0) return true;
    }

    return false;
}

bool ok(int64 a, int64 b, int64 c) {
    return check_mul(a, b, c) || check_mul(b, a, c) || check_mul(c, a, b);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int t;
    if (!(cin >> t)) return 0;
    while (t--) {
        int64 a, b, c;
        cin >> a >> b >> c;
        cout << (ok(a, b, c) ? "YES" : "NO") << '\n';
    }
    return 0;
}
```