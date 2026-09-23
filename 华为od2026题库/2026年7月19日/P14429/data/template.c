#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define MAX_LEN 200000

int main() {
    char line[MAX_LEN];
    if (!fgets(line, MAX_LEN, stdin)) return 0;

    int len = (int)strlen(line);
    while (len > 0 && (line[len - 1] == '\n' || line[len - 1] == '\r'))
        line[--len] = '\0';

    // 顶层逗号（括号深度为 0 时的第一个逗号）分隔 n 与乘客列表
    int comma = -1;
    int bracket = 0;
    for (int i = 0; i < len; i++) {
        if (line[i] == '[') bracket++;
        else if (line[i] == ']') bracket--;
        else if (line[i] == ',' && bracket == 0) { comma = i; break; }
    }

    int n = atoi(line);  // 逗号之前即为整数 n
    const char* rest = line + comma + 1;

    // 提取所有整数并两两配对为 [起点,终点]
    int cap = 16, total = 0;
    int* flat = (int*)malloc(cap * sizeof(int));
    int num = 0, have = 0;
    for (int i = 0; rest[i]; i++) {
        char c = rest[i];
        if (isdigit((unsigned char)c)) {
            num = num * 10 + (c - '0');
            have = 1;
        } else if (have) {
            if (total >= cap) { cap *= 2; flat = (int*)realloc(flat, cap * sizeof(int)); }
            flat[total++] = num;
            num = 0; have = 0;
        }
    }
    if (have) {
        if (total >= cap) { cap *= 2; flat = (int*)realloc(flat, cap * sizeof(int)); }
        flat[total++] = num;
    }

    int rows = total / 2;
    int** passengers = (int**)malloc(rows * sizeof(int*));
    int* colSize = (int*)malloc(rows * sizeof(int));
    for (int i = 0; i < rows; i++) {
        passengers[i] = (int*)malloc(2 * sizeof(int));
        passengers[i][0] = flat[2 * i];
        passengers[i][1] = flat[2 * i + 1];
        colSize[i] = 2;
    }

    int result = maxRideProfit(n, passengers, rows, colSize);
    printf("%d\n", result);

    for (int i = 0; i < rows; i++) free(passengers[i]);
    free(passengers);
    free(colSize);
    free(flat);
    return 0;
}
