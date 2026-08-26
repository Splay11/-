#pragma GCC optimize("O3")
#pragma GCC optimize("Ofast")
#pragma GCC optimize("unroll-loops")
#pragma GCC target("avx,avx2,fma")

#include <bits/stdc++.h>

using namespace std;

#define out(x) cout << #x << '=' << (x) << endl
#define out2(x, y) cout << #x << '=' << (x) << ',' << #y << '=' << (y) << endl 
#define no cout << "No" << endl; return
#define yes cout << "Yes" << endl; return
#define outvec(a) for (auto &v : (a)) { cout << v << ' '; } cout << endl
#define lowbit(x) ((x) & -(x))
#define gcd __gcd 
#define inf 0x3f3f3f3f3f3f3f3fLL
#define infi 0x3f3f3f3f

using ll = long long;
using pii = pair<int, int>;

template<typename T> ostream & operator << (ostream &out,const set<T>&obj){out<<"set(";for(auto it=obj.begin();it!=obj.end();it++) out<<(it==obj.begin()?"":", ")<<*it;out<<")";return out;}
template<typename T1,typename T2> ostream & operator << (ostream &out,const map<T1,T2>&obj){out<<"map(";for(auto it=obj.begin();it!=obj.end();it++) out<<(it==obj.begin()?"":", ")<<it->first<<": "<<it->second;out<<")";return out;}
template<typename T1,typename T2> ostream & operator << (ostream &out,const pair<T1,T2>&obj){out<<"<"<<obj.first<<", "<<obj.second<<">";return out;}
template<typename T> ostream & operator << (ostream &out,const vector<T>&obj){out<<"vector(";for(auto it=obj.begin();it!=obj.end();it++) out<<(it==obj.begin()?"":", ")<<*it;out<<")";return out;}


void solve() {
	int n, k;
	cin >> n >> k;
	map<int, int> m;
	for (int i = 1; i <= n; i++) {
		int x;
		cin >> x;
		x %= k;
		m[x]++;
	}
	int ans = m[0];
	m.erase(0);
	for (pii p : m) {
		int a = p.first;
		int b = (k - a) % k;
		if (a == b) {
			int d = m[a] / 2;
			m[a] %= 2;
			ans += d;
		} else if (m.count(b)) {
			int d = min(m[a], m[b]);
			m[a] -= d;
			m[b] -= d;
			ans += d;
		}
	}
	cout << ans << endl;
}
 
int main(void) {
    ios::sync_with_stdio(false);
    cin.tie(0); cout.tie(0);
    int t = 1;
	//cin >> t;
    
    while (t--) {
    	solve(); 
	}
}