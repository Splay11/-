#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "foo.c"

#define MAX_LEN 2048

int main() {
    char s[MAX_LEN];
    if (!fgets(s, MAX_LEN, stdin)) return 1;

    // 去除末尾可能的换行符
    int len = strlen(s);
    if (len > 0 && s[len - 1] == '\n') s[--len] = '\0';

    // 统计 n：数 '[' 的数量减 1（最外层方括号）
    int n = 0;
    for (int i = 0; i < len; i++)
        if (s[i] == '[') n++;
    n--;

    // 分配二维数组空间
    int** grid = (int**)malloc(n * sizeof(int*));
    for (int i = 0; i < n; i++)
        grid[i] = (int*)calloc(n, sizeof(int));

    int depth = 0, row = 0, col = 0, num = 0, inNum = 0;
    for (int i = 0; i < len; i++) {
        char c = s[i];
        if (c == '[') {
            depth++;
            if (depth == 2) col = 0;  // 进入新一行，列号归零
        } else if (c == ']') {
            if (inNum) { grid[row][col++] = num; num = 0; inNum = 0; }
            if (depth == 2) row++;    // 当前行结束，行号加一
            depth--;
        } else if (c >= '0' && c <= '9') {
            num = num * 10 + (c - '0');
            inNum = 1;
        } else if (c == ',' && inNum && depth == 2) {
            // 行内逗号分隔，结算当前数字
            grid[row][col++] = num;
            num = 0; inNum = 0;
        }
    }

    int result = countMinefields(grid, n);
    printf("%d\n", result);

    // 释放内存
    for (int i = 0; i < n; i++) free(grid[i]);
    free(grid);
    return 0;
}
