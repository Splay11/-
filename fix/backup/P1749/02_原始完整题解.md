## 思路：模拟 小根堆 multiset
本题由于每一次操作都需要使用数组的最小值，因此我们可以使用小根堆或者multiset这种数据结构去模拟，具体的操作方式是每次弹出堆中/multiset中的最小值，然后加上$b_j$，对于小根堆而言还需要维护一个变量来动态更新最大值，对于multiset而言可以直接使用`*rbegin()*来获取最大值

C++
```cpp
#include<bits/stdc++.h>
#define fr(i,a,b) for(int i=a;i<=b;i++)
#define int long long
using namespace std ;

signed main() {
    ios::sync_with_stdio(false) ;
    int n, m ;
    cin >> n >> m ;
    multiset<int> st ; 
    fr(i, 1, n) {
        int x ;
        cin >> x ;
        st.insert(x) ; 
    }
    while (m--) {
        auto x = *st.begin() ; 
        st.erase(st.begin()) ; 
        int p  ;cin>>p ; 
        x+=p ; 
        st.insert(x) ; 
        cout<<*st.rbegin()<<endl;
    }


}
```