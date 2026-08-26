## 解题思路

甲组策略固定为每轮取当前剩余货箱中分值最高者；乙组最优策略也是每轮取当前最大值，否则会把更大的分值留给甲组，差值不会更小。

因此将 $v_i$ 降序排序后，双方按顺序轮流取：

- 甲组取第 $1,3,5,\ldots$ 个；
- 乙组取第 $2,4,6,\ldots$ 个。

答案即为两者累计分值之差。

## 复杂度分析

- 时间：排序 $O(m \log m)$，求和 $O(m)$。
- 空间：$O(m)$。

## 代码实现

### Python

```python
import sys


def solve_case(m, vals):
    vals.sort(reverse=True)
    team_a = team_b = 0
    for i in range(m):
        if i % 2 == 0:
            team_a += vals[i]
        else:
            team_b += vals[i]
    return team_a - team_b


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    t, idx = data[0], 1
    ans = []
    for _ in range(t):
        m = data[idx]
        idx += 1
        vals = data[idx:idx + m]
        idx += m
        ans.append(str(solve_case(m, vals)))
    sys.stdout.write("\n".join(ans))


if __name__ == "__main__":
    main()
```

### Java

```java
import java.io.*;
import java.util.*;

public class Main {
    static long solveCase(int m, int[] vals) {
        Arrays.sort(vals);
        long teamA = 0, teamB = 0;
        boolean aTurn = true;
        for (int i = m - 1; i >= 0; i--) {
            if (aTurn) teamA += vals[i];
            else teamB += vals[i];
            aTurn = !aTurn;
        }
        return teamA - teamB;
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int T = Integer.parseInt(br.readLine());
        StringBuilder sb = new StringBuilder();
        while (T-- > 0) {
            int m = Integer.parseInt(br.readLine());
            String[] parts = br.readLine().split(" ");
            int[] vals = new int[m];
            for (int i = 0; i < m; i++) vals[i] = Integer.parseInt(parts[i]);
            sb.append(solveCase(m, vals)).append('\n');
        }
        System.out.print(sb);
    }
}
```

### C++

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

long long solve_case(int m, vector<int>& vals) {
    sort(vals.begin(), vals.end(), greater<int>());
    long long team_a = 0, team_b = 0;
    for (int i = 0; i < m; i++) {
        if (i % 2 == 0) team_a += vals[i];
        else team_b += vals[i];
    }
    return team_a - team_b;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int T;
    cin >> T;
    while (T--) {
        int m;
        cin >> m;
        vector<int> vals(m);
        for (int i = 0; i < m; i++) cin >> vals[i];
        cout << solve_case(m, vals) << '\n';
    }
    return 0;
}
```