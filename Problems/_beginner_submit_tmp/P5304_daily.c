#include <stdlib.h>
#include <string.h>

int maxDropoffReach(int n, int** links, int linksSize, int* linksColSize, int* width, int widthSize) {
    (void)linksColSize; (void)widthSize;
    if (n <= 0) return 0;
    int* deg = (int*)calloc(n, sizeof(int));
    for (int i = 0; i < linksSize; i++) { deg[links[i][0]]++; deg[links[i][1]]++; }
    int** g = (int**)malloc(n * sizeof(int*));
    int* gc = (int*)calloc(n, sizeof(int));
    for (int i = 0; i < n; i++) g[i] = (int*)malloc((deg[i] ? deg[i] : 1) * sizeof(int));
    for (int i = 0; i < linksSize; i++) {
        int u = links[i][0], v = links[i][1];
        g[u][gc[u]++] = v; g[v][gc[v]++] = u;
    }
    int** ch = (int**)malloc(n * sizeof(int*));
    int* cc = (int*)calloc(n, sizeof(int));
    int* parent = (int*)malloc(n * sizeof(int));
    for (int i = 0; i < n; i++) { parent[i] = -1; ch[i] = (int*)malloc((deg[i] ? deg[i] : 1) * sizeof(int)); }
    int* q = (int*)malloc(n * sizeof(int));
    int qh = 0, qt = 0;
    q[qt++] = 0; parent[0] = -2;
    while (qh < qt) {
        int u = q[qh++];
        for (int i = 0; i < gc[u]; i++) {
            int v = g[u][i];
            if (parent[v] == -1) { parent[v] = u; ch[u][cc[u]++] = v; q[qt++] = v; }
        }
    }
    char* vis0 = (char*)calloc(n, 1);
    char* vis1 = (char*)calloc(n, 1);
    char* seen = (char*)calloc(n, 1);
    int* su = (int*)malloc(2 * n * sizeof(int));
    int* sc = (int*)malloc(2 * n * sizeof(int));
    int top = 0;
    su[top] = 0; sc[top] = 0; top++; vis0[0] = 1;
    while (top > 0) {
        top--; int u = su[top], used = sc[top];
        seen[u] = 1;
        for (int i = 0; i < cc[u]; i++) {
            int v = ch[u][i], nu;
            if (width[u] > width[v]) nu = used;
            else if (used == 0) nu = 1;
            else continue;
            char* vv = (nu == 0 ? vis0 : vis1);
            if (!vv[v]) { vv[v] = 1; su[top] = v; sc[top] = nu; top++; }
        }
    }
    int ans = 0;
    for (int i = 0; i < n; i++) if (seen[i]) ans++;
    for (int i = 0; i < n; i++) { free(g[i]); free(ch[i]); }
    free(g); free(ch); free(deg); free(gc); free(cc); free(parent); free(q);
    free(vis0); free(vis1); free(seen); free(su); free(sc);
    return ans;
}
