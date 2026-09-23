#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAXN 500505
#define MAXE 1500005
#define MAXADJ 3000005

int head[MAXN], to[MAXADJ], nxt[MAXADJ], which[MAXADJ], ecnt;
char used[MAXE];
int ptr[MAXN];
int stk[MAXE + 5];
int circ[MAXE + 5];

void add_half(int a, int b, int eid) {
    to[ecnt] = b;
    which[ecnt] = eid;
    nxt[ecnt] = head[a];
    head[a] = ecnt++;
}

void add_edge(int a, int b, int eid) {
    add_half(a, b, eid);
    add_half(b, a, eid);
}

/* 按层搭建三角栈道，求从 start 出发的无向欧拉回路，写入 circ，返回长度 */
int solve(int h, int start) {
    int n = h * (h + 1) / 2;
    int i, r, c, u, v, w, eid, m, top, clen, x, a, b;
    for (i = 1; i <= n; i++) {
        head[i] = -1;
        ptr[i] = -2; /* 稍后设为 head[i] */
    }
    ecnt = 0;
    eid = 0;
    for (r = 2; r <= h; r++) {
        int base = r * (r - 1) / 2;
        int prev = (r - 1) * (r - 2) / 2;
        for (c = 1; c < r; c++) {
            u = base + c;
            v = base + c + 1;
            w = prev + c;
            /* 同层相邻，以及接到上一层同一台位的两条斜栈道 */
            add_edge(u, v, eid++);
            add_edge(u, w, eid++);
            add_edge(v, w, eid++);
        }
    }
    m = eid;
    memset(used, 0, m);
    for (i = 1; i <= n; i++) {
        ptr[i] = head[i];
    }
    top = 0;
    clen = 0;
    stk[top++] = start;
    /* Hierholzer：沿未用边走，走不通时把点弹入回路（得到逆序） */
    while (top) {
        u = stk[top - 1];
        while (ptr[u] != -1 && used[which[ptr[u]]]) {
            ptr[u] = nxt[ptr[u]];
        }
        if (ptr[u] == -1) {
            circ[clen++] = u;
            top--;
        } else {
            int e = which[ptr[u]];
            x = to[ptr[u]];
            ptr[u] = nxt[ptr[u]];
            used[e] = 1;
            stk[top++] = x;
        }
    }
    /* 逆序得到从起点出发的回路 */
    for (i = 0; i < clen / 2; i++) {
        a = circ[i];
        b = circ[clen - 1 - i];
        circ[i] = b;
        circ[clen - 1 - i] = a;
    }
    (void)start;
    return clen;
}

int main(void) {
    int k, t, h, s, len, i;
    if (scanf("%d", &k) != 1) {
        return 0;
    }
    for (t = 0; t < k; t++) {
        scanf("%d %d", &h, &s);
        len = solve(h, s);
        for (i = 0; i < len; i++) {
            if (i) {
                putchar(' ');
            }
            printf("%d", circ[i]);
        }
        putchar('\n');
    }
    return 0;
}
