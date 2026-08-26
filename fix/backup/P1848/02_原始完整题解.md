## 题解

贪心

对于每个房子按照舒适度排序从大到小排序，对于其价格 $x$，找到所有人中持有的金币第一个 $ \ge x$ 的(用二分实现)，表示最适合买当前房子的人，并将其删去即可。

在cpp中动态删除和二分的过程可以用 `multiset` 来实现

整体时间复杂度: $O(n \log n)$

## AC代码

- CPP

```cpp
#include <bits/stdc++.h>

using namespace std;

#define int long long
signed main() {
    int n, m;
    cin >> n >> m;
    multiset<int> ms;
    for(int i = 0; i < n; i ++)
    {
    	int x; cin >> x;
    	ms.insert(x);
    }
    vector<array<int, 2>> h(m);
    for(auto&[l, r] : h) cin >> l >> r;
	sort(h.begin(), h.end(), greater<array<int, 2>>());
    int res = 0;
	for(auto& [l, r] : h)
	{
		auto ite = ms.lower_bound(r);
		if(ite != ms.end())
			res += l, ms.erase(ite);
	}
 	cout << res << "\n";
    return 0;
}
```
### java
```java
import java.util.*;
import java.util.stream.Collectors;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n =sc.nextInt(),m = sc.nextInt();
        int[] friend = new int[n];
        for(int i =0;i<n;i++) friend[i] = sc.nextInt();
        int[][] house = new int[m][2];
        for(int i=0;i<m;i++){
            for(int j=0;j<2;j++){
                house[i][j] = sc.nextInt();
            }
        }

        GetRes_(house,friend);

    }

    private static void GetRes_(int[][] house, int[] friend) {

        Arrays.sort(friend);
        Arrays.sort(house,(a,b)->a[1]-b[1]);

        PriorityQueue<Integer> queue = new PriorityQueue<>(Collections.reverseOrder());
        long res=0;
        int index=0;
        for(int fri:friend){
            while(index< house.length && fri>=house[index][1]){
                queue.add(house[index][0]);
                index++;
            }
            res+=(queue.size()==0?0: queue.poll());
        }
        System.out.println(res);

    }
}
```