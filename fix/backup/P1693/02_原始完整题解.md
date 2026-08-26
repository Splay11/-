## 题目思路

通过给出的字符串可以计算得到每一个字符的数量，那么"you"重排之后可以出现的最大次数其实就是'y','o','u'的数量的最小值。

得到"you"出现的最大数量之后，由于不需要注重顺序，把对应数量的"you"先打印，剩下的字符再后面打印即可。

## 代码

**Java**

~~~java
import java.util.HashMap;
import java.util.Map;
import java.util.Scanner;

public class Main {
    public static void solve() {
        Scanner scanner = new Scanner(System.in);
        String s = scanner.next();
        Map<Character, Integer> h = new HashMap<>();
        for (char c : s.toCharArray()) {
            h.put(c, h.getOrDefault(c, 0) + 1);
        }
        int youCnt = Math.min(Math.min(h.getOrDefault('y', 0), h.getOrDefault('o', 0)), h.getOrDefault('u', 0));
        StringBuilder ans = new StringBuilder();
        h.put('y', h.getOrDefault('y', 0) - youCnt);
        h.put('o', h.getOrDefault('o', 0) - youCnt);
        h.put('u', h.getOrDefault('u', 0) - youCnt);
        while (youCnt-- > 0) {
            ans.append("you");
        }
        for (Map.Entry<Character, Integer> t : h.entrySet()) {
        	int cnt = t.getValue();
            while (cnt -- > 0) {
                ans.append(t.getKey());
            }
        }
        System.out.println(ans.toString());
    }

    public static void main(String[] args) {
        int T = 1;
        while (T-- > 0) {
            solve();
        }
    }
}

~~~

**C++**

~~~c++
#include<bits/stdc++.h>

using namespace std;

#define endl '\n'

void solve() {
	string s;
	cin >> s;
	map<char, int> h;
	for (char c: s) ++ h[c];
	int you_cnt = min({h['y'], h['o'], h['u']});
	string ans;
	h['y'] -= you_cnt;
	h['o'] -= you_cnt;
	h['u'] -= you_cnt;
	while(you_cnt --) {
		ans += "you";	
	}
	for (auto t: h) {
		while(t.second --) {
			ans += t.first;
		}
	}
	cout << ans << endl;
}

signed main() {
	int T = 1;
	while(T --) {
		solve();
	}
}
~~~

**Python**

~~~python
def solve():
    s = input()
    h = {}
    for c in s:
        h[c] = h.get(c, 0) + 1
    you_cnt = min(h.get('y', 0), h.get('o', 0), h.get('u', 0))
    ans = ''
    h['y'] = h.get('y', 0) - you_cnt
    h['o'] = h.get('o', 0) - you_cnt
    h['u'] = h.get('u', 0) - you_cnt
    ans += 'you' * you_cnt
    for t in h.items():
        ans += t[0] * t[1]
    print(ans)

T = 1
while T > 0:
    solve()
    T -= 1
~~~

**会员可通过查看《已通过》的提交记录来查看其他语言哦~**