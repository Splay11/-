## 解题思路

### 二分半径 + 扫描线

* **思路概览**：将答案 $r$ 用二分搜索，在每个候选半径上判断能否在 $x$ 轴或 $y$ 轴上放置圆心，使得被覆盖点数 $\ge k$，其中 $k=\lceil n/2\rceil$。
* **可行性检查**：

  1. 对给定半径 $r$，分别在两条轴上判断：

     * **横轴情况（axis=0）**：圆心 $(c,0)$ 覆盖点 $(x_i,y_i)$ 的条件是 $|y_i|\le r$ 且 $|c - x_i|\le \sqrt{r^2 - y_i^2}$，从而得到在 $c$ 轴上的区间 $[x_i - d_i,x_i + d_i]$。
     * **纵轴情况（axis=1）**：圆心 $(0,c)$ 覆盖点条件是 $|x_i|\le r$ 且 $|c - y_i|\le \sqrt{r^2 - x_i^2}$，区间为 $[y_i - d_i,y_i + d_i]$。
  2. 将所有区间的左右端点作为事件：左端记 $+1$，右端记 $-1$，对事件按坐标升序（同点时“+1”先于“-1”）排序并扫描，记录最大同时覆盖数。若某一轴上最大覆盖数 $\ge k$，则该 $r$ 可行。
* **二分搜索**：

  * 初始区间 $[0, R]$，$R$ 可设为 $\sqrt{(2\cdot10^5)^2+(2\cdot10^5)^2}$$\approx3\times10^5$。
  * 重复约 $60$ 次，直到区间长度 $\le10^{-6}$。

## 复杂度分析

* 每次可行性检查：遍历 $n$ 点生成最多 $2n$ 事件，排序 $O(n\log n)$，扫描 $O(n)$，共 $O(n\log n)$。
* 二分约 $60$ 轮，总体 $O(60,n\log n)=O(n\log n)$，可在 $n\le10^5$ 下通过。

## 代码实现

### Python

```python
import sys, math

def check(r, pts, k):
    # axis=0 横轴；axis=1 纵轴
    def scan(axis):
        ev = []
        for x, y in pts:
            # 按轴判断
            if axis == 0:
                if abs(y) > r: continue
                d = math.sqrt(r*r - y*y)
                L, R = x - d, x + d
            else:
                if abs(x) > r: continue
                d = math.sqrt(r*r - x*x)
                L, R = y - d, y + d
            ev.append((L, 1))
            ev.append((R, -1))
        if len(ev) < 2*k: 
            return False
        ev.sort(key=lambda e: (e[0], -e[1]))
        cnt = 0
        for _, v in ev:
            cnt += v
            if cnt >= k:
                return True
        return False

    # 只要任一轴可行即返回 True
    return scan(0) or scan(1)

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    pts = [(float(data[i]), float(data[i+1])) for i in range(1, 2*n, 2)]
    k = (n + 1) // 2
    lo, hi = 0.0, 3e5
    for _ in range(60):
        mid = (lo + hi) / 2
        if check(mid, pts, k):
            hi = mid
        else:
            lo = mid
    print("{:.6f}".format(hi))

if __name__ == "__main__":
    main()
```

### Java

```java
import java.io.*;
import java.util.*;

public class Main {
    static int n, k;
    static double[] xs, ys;

    // 判断半径 r 是否可行
    static boolean check(double r) {
        // scan 对某条轴（axis=0 横，1 纵）做事件扫描
        for (int axis = 0; axis < 2; axis++) {
            List<double[]> ev = new ArrayList<>();
            for (int i = 0; i < n; i++) {
                double d0 = axis == 0 ? Math.abs(ys[i]) : Math.abs(xs[i]);
                if (d0 > r) continue;
                double d = Math.sqrt(r*r - d0*d0);
                double mid = axis == 0 ? xs[i] : ys[i];
                ev.add(new double[]{mid - d, 1});
                ev.add(new double[]{mid + d, -1});
            }
            if (ev.size() < 2*k) continue;
            ev.sort((a, b) -> {
                if (a[0] != b[0]) return Double.compare(a[0], b[0]);
                return Double.compare(b[1], a[1]);
            });
            int cnt = 0;
            for (double[] e : ev) {
                cnt += (int)e[1];
                if (cnt >= k) return true;
            }
        }
        return false;
    }

    public static void main(String[] args) throws Exception {
        BufferedReader in = new BufferedReader(new InputStreamReader(System.in));
        n = Integer.parseInt(in.readLine().trim());
        xs = new double[n];
        ys = new double[n];
        for (int i = 0; i < n; i++) {
            String[] sp = in.readLine().split("\\s+");
            xs[i] = Double.parseDouble(sp[0]);
            ys[i] = Double.parseDouble(sp[1]);
        }
        k = (n + 1) / 2;
        double lo = 0, hi = 3e5;
        for (int it = 0; it < 60; it++) {
            double mid = (lo + hi) / 2;
            if (check(mid)) hi = mid;
            else lo = mid;
        }
        System.out.printf("%.6f\n", hi);
    }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

int n, k;
vector<double> xs, ys;

// 判断给定半径 r 是否能在任一轴上覆盖 >=k 个点
bool check(double r) {
    for (int axis = 0; axis < 2; axis++) {
        vector<pair<double,int>> ev;
        for (int i = 0; i < n; i++) {
            double d0 = axis == 0 ? fabs(ys[i]) : fabs(xs[i]);
            if (d0 > r) continue;
            double d = sqrt(r*r - d0*d0);
            double mid = axis == 0 ? xs[i] : ys[i];
            ev.emplace_back(mid - d, +1);
            ev.emplace_back(mid + d, -1);
        }
        if ((int)ev.size() < 2*k) continue;
        sort(ev.begin(), ev.end(), [](auto &a, auto &b){
            if (a.first != b.first) return a.first < b.first;
            return a.second > b.second;
        });
        int cnt = 0;
        for (auto &e : ev) {
            cnt += e.second;
            if (cnt >= k) return true;
        }
    }
    return false;
}

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> n;
    xs.resize(n); ys.resize(n);
    for (int i = 0; i < n; i++) {
        cin >> xs[i] >> ys[i];
    }
    k = (n + 1) / 2;
    double lo = 0.0, hi = 3e5;
    for (int it = 0; it < 60; it++) {
        double mid = (lo + hi) / 2;
        if (check(mid)) hi = mid;
        else lo = mid;
    }
    cout << fixed << setprecision(6) << hi << "\n";
    return 0;
}
```