#include <stdio.h>
#include <string.h>

#define MAXN 100005

char s[MAXN];

// 滑动窗口：对每个右端点，无重复窗口内长度为 k 及以上的子串个数可 O(1) 计算
long long count_unique(int n, int k) {
    int last[26];
    int i, left = 0;
    long long ans = 0;
    // last[c]：字符 c 上一次出现的下标，-1 表示还没出现过
    for (i = 0; i < 26; i++) {
        last[i] = -1;
    }
    for (i = 0; i < n; i++) {
        int idx = s[i] - 'a';
        // 窗口内出现重复，把左端推到上一次该字符的右边
        if (last[idx] >= left) {
            left = last[idx] + 1;
        }
        last[idx] = i;
        // 以 i 为右端、长度 >= k 的起点最多到 i-k+1，且不能小于 left
        int limit = i - k + 1;
        if (limit >= left) {
            ans += (long long)(limit - left + 1);
        }
    }
    return ans;
}

int main(void) {
    int k, n;
    scanf("%s", s);
    scanf("%d", &k);
    n = (int)strlen(s);
    printf("%lld\n", count_unique(n, k));
    return 0;
}
