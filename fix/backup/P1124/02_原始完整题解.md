## 思路

将a数组按照b数组的值分组，每组内对应c数组中1~n的数字是固定的，组内就变成了两个数组匹配，差绝对值的和最小，这是一个经典的贪心问题，直接将两个数组排序后对应位置匹配即可，证明略。

## 代码

### c++

~~~c++
#include <bits/stdc++.h>
using namespace std;

vector<int> v[3];		//按b数组0、1、2分组
int main()
{
	int n;
	cin >> n;
	vector<int> a(n);
	vector<int> b(n);
	for(int &t: a) cin >> t;
	for(int i = 0 ; i < n ; i ++) {
		cin >> b[i];		//此处的值对应b数组
		v[b[i]].push_back(a[i]);
	}
	int x = 0;	//c数组的值
	long long ans = 0;
	for(int i = 0 ; i < 3 ; i ++) {
		sort(v[i].begin(), v[i].end());		//组内排序，和c数组从1开始匹配
		for(int t: v[i]) {
			x++;
			ans += abs(t - x);		//记录答案
		}
	}
	cout << ans << endl;
}
~~~



### java

~~~java
import java.util.*;
public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        int[] a = new int[n], b = new int[n];
        for (int i = 0; i < n; i++) {
            a[i] = sc.nextInt();
        }
        List<Integer>[] v = new List[3];
        for (int i = 0, now = 1; i < 3; i++) {
            v[i] = new ArrayList<>();
        }
        for (int i = 0; i < n; i++) {
        	b[i] = sc.nextInt();
            v[b[i]].add(a[i]);
        }
        long ans = 0, x = 0;
        for (int i = 0; i < 3; i++) {
            v[i].sort(null);
            for(int t: v[i]) {
            	x++;
                ans += Math.abs(t - x);
            }
        }
        System.out.println(ans);
    }
}
~~~