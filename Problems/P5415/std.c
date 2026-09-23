#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAXE 320
#define MAXN 640
#define MAXL 24

static const char START[] = "Core-SW-01";

char names[MAXN][MAXL];
int nnode;
int adj[MAXN][MAXE];
int adjn[MAXN];
int cur[MAXN];
int us[MAXE], vs[MAXE];
int st[MAXE + 8];
int route[MAXE + 8];

int get_id(const char *s) {
    int i;
    for (i = 0; i < nnode; i++) {
        if (strcmp(names[i], s) == 0) {
            return i;
        }
    }
    strcpy(names[nnode], s);
    nnode++;
    return nnode - 1;
}

int cmp_asc(const void *a, const void *b) {
    int ia = *(const int *)a;
    int ib = *(const int *)b;
    return strcmp(names[ia], names[ib]);
}

void find_path(int start, int *nroute) {
    int nst = 0;
    *nroute = 0;
    st[nst++] = start;
    while (nst) {
        int u = st[nst - 1];
        if (cur[u] < adjn[u]) {
            /* 出边已按终点名字从小到大排，按下标依次取，先走更小的终点 */
            /* 有未用跳转就继续往前走，把终点压栈 */
            /* 没有出边才记下当前点，相当于后序，死胡同会先出现在答案尾部 */
            /* 这样不会像纯贪心那样走进死胡同就再也回不来 */
            int v = adj[u][cur[u]++];
            st[nst++] = v;
        } else {
            route[(*nroute)++] = u;
            nst--;
        }
    }
}

int main(void) {
    char u[MAXL], v[MAXL];
    int m = 0;
    int i, start, nroute;
    nnode = 0;
    memset(adjn, 0, sizeof(adjn));
    memset(cur, 0, sizeof(cur));
    while (scanf("%23s%23s", u, v) == 2) {
        us[m] = get_id(u);
        vs[m] = get_id(v);
        m++;
    }
    for (i = 0; i < m; i++) {
        adj[us[i]][adjn[us[i]]++] = vs[i];
    }
    for (i = 0; i < nnode; i++) {
        qsort(adj[i], (size_t)adjn[i], sizeof(int), cmp_asc);
    }
    start = get_id(START);
    find_path(start, &nroute);
    for (i = nroute - 1; i >= 0; i--) {
        if (i != nroute - 1) {
            putchar(' ');
        }
        printf("%s", names[route[i]]);
    }
    putchar('\n');
    return 0;
}
