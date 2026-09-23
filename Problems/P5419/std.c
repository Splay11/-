/* 偶数长度窗口上 0/1 数量相等：交错串 0101... 一定合法 */
#include <stdio.h>

#define MAXN 100005

char s[MAXN];

void build_balanced_01(int k) {
    int i;
    /* 灯位从 1 开始：奇数位放 0，偶数位放 1 */
    for (i = 1; i <= k; i++) {
        s[i - 1] = (i % 2 == 1) ? '0' : '1';
    }
    s[k] = '\0';
}

int main(void) {
    int k, q, i, a, b;
    /* 第一行灯带长度，第二行窗口条数 */
    scanf("%d", &k);
    scanf("%d", &q);
    /* 窗口写成 a,b，交错串对所有窗口都成立，读掉即可 */
    for (i = 0; i < q; i++) {
        scanf("%d,%d", &a, &b);
    }
    build_balanced_01(k);
    printf("%s\n", s);
    return 0;
}
