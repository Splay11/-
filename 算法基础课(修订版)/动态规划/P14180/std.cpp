#include <bits/stdc++.h>
using namespace std;

const int maxn=1e3+10;
int dp[maxn];
int n;
struct node{
	int l, w, h;
}box[maxn];


int main(){
    cin>>n;
    for(int i=1;i<=n;++i){
    	cin>>box[i].l>>box[i].w>>box[i].h;
	}
    //长、宽、高的三个优先级进行从小到大的排序
    sort(box+1, box+n+1, [&](node a, node b){
		if(a.l!=b.l){
			return a.l<b.l;   
		}
		if(a.w!=b.w){
			return a.w<b.w;
		}
		return a.h<b.h;
	});
    int ans=0;
    //dp[i]表示放上第i个盒子所能达到的最大高度
    for(int i=1;i<=n;++i){
        dp[i]=box[i].h;
        for (int j = 1; j < i; j++) {
            if (box[i].h > box[j].h && box[i].l > box[j].l && box[i].w > box[j].w) {
                dp[i]=max(dp[i],dp[j]+box[i].h);
            }
        }
        ans = max(ans,dp[i]);
    }
    cout<<ans;
}
