#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define MAX_TOKENS 4000  // n,m,w + 最多 1000 条边×3 = 3003

// 从字符串提取所有整数（忽略非数字字符）
static int extractInts(const char* s, int* out) {
    int cnt = 0, cur = 0, have = 0;
    for (int i = 0; s[i]; i++) {
        char c = s[i];
        if (isdigit((unsigned char)c)) {
            cur = cur * 10 + (c - '0');
            have = 1;
        } else if (have) {
            out[cnt++] = cur;
            cur = 0;
            have = 0;
        }
    }
    if (have) out[cnt++] = cur;
    return cnt;
}

int minCost(int n, int m, int w, int** roads, int roadsSize, int* roadsColSize);

int main() {
    char line[65536];
    if (!fgets(line, sizeof(line), stdin)) return 0;
    int len = (int)strlen(line);
    while (len > 0 && (line[len - 1] == '\n' || line[len - 1] == '\r'))
        line[--len] = '\0';

    // 提取全部整数：前 3 个为 n, m, w，其余每 3 个为一条路线
    int a[MAX_TOKENS];
    int cnt = extractInts(line, a);
    int n = a[0], m = a[1], w = a[2];
    int roadsSize = (cnt - 3) / 3;

    int** roads = (int**)malloc(roadsSize * sizeof(int*));
    int* roadsColSize = (int*)malloc(roadsSize * sizeof(int));
    for (int i = 0; i < roadsSize; i++) {
        roads[i] = (int*)malloc(3 * sizeof(int));
        roads[i][0] = a[3 + i * 3];
        roads[i][1] = a[3 + i * 3 + 1];
        roads[i][2] = a[3 + i * 3 + 2];
        roadsColSize[i] = 3;
    }

    int ans = minCost(n, m, w, roads, roadsSize, roadsColSize);
    printf("%d\n", ans);

    for (int i = 0; i < roadsSize; i++) free(roads[i]);
    free(roads);
    free(roadsColSize);
    return 0;
}
