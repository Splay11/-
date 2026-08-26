# 题解

贡献法计数

对于一个长度为 $n$ 的字符串 $|S|$，记字符 $c$ 出现的次数为 $cnt[c]$，那么对答案的贡献为 $(2 ^ {cnt[c]} - 1) \cdot (2 ^ {n - cnt[c]})$，即当前字符最少选一个，其他字符任意选，最终将答案累加即可。 
 

# AC代码

## Python

```python
def main():
    import sys
    input = sys.stdin.read
    data = input().strip()
    
    mod = 10**9 + 7
    n = len(data)
    
    from collections import Counter
    cnt = Counter(data)
    
    res = 0
    for c in cnt:
        r = cnt[c]
        res = (res + (pow(2, r, mod) - 1) * pow(2, n - r, mod)) % mod
    
    print(res)

if __name__ == "__main__":
    main()
```

## Java

```java
import java.util.*;

public class Main {
    static final int MOD = 1000000007;

    public static long qmi(long a, long b) {
        long res = 1 % MOD;
        while (b > 0) {
            if ((b & 1) == 1) res = res * a % MOD;
            a = a * a % MOD;
            b >>= 1;
        }
        return res;
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        String s = scanner.next();
        
        Map<Character, Integer> mp = new HashMap<>();
        for (char ch : s.toCharArray()) {
            mp.put(ch, mp.getOrDefault(ch, 0) + 1);
        }
        
        long res = 0;
        int n = s.length();
        for (Map.Entry<Character, Integer> entry : mp.entrySet()) {
            int r = entry.getValue();
            res = (res + (qmi(2, r) - 1) * qmi(2, n - r)) % MOD;
        }
        
        System.out.println(res);
    }
}
```

## C++

```cpp
#include <bits/stdc++.h>

using namespace std;

typedef long long LL;
const int mod = 1e9 + 7;

LL qmi(LL a, LL b) {
    LL res = 1 % mod;
    while (b) {
        if (b & 1) res = res * a % mod;
        a = a * a % mod;
        b >>= 1;
    }
    return res;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(0);
    
    string s;
    cin >> s;
    unordered_map<char, int> mp;
    for (auto ch : s) mp[ch]++;
    
    LL res = 0;
    int n = s.size();
    for (auto [l, r] : mp)
        res = (res + (qmi(2, r) - 1) * qmi(2, n - r)) % mod;
    
    cout << res << "\n";
    
    return 0;
}
```