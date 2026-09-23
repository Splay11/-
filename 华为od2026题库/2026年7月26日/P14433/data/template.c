#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#define MAX_LEN 300000

// 前向声明用户函数
int* sortArrayByParity(int* nums, int numsSize, int* returnSize);

int main() {
    char line[MAX_LEN];
    if (!fgets(line, MAX_LEN, stdin)) return 1;
    int len = strlen(line);
    while (len > 0 && (line[len - 1] == '\n' || line[len - 1] == '\r'))
        line[--len] = '\0';

    // 解析 JSON 数组 [a,b,c,...]
    int* nums = (int*)malloc(20000 * sizeof(int));
    int n = 0;
    int i = 1; // 跳过 '['
    while (i < len) {
        char c = line[i];
        if (c == ']') break;
        if (c == ',' || c == ' ') {
            i++;
            continue;
        }
        // 读取整数（可能含负号，但本题值域 >= 0）
        int val = 0;
        while (i < len && line[i] >= '0' && line[i] <= '9') {
            val = val * 10 + (line[i] - '0');
            i++;
        }
        nums[n++] = val;
    }

    int returnSize;
    int* res = sortArrayByParity(nums, n, &returnSize);

    // 输出 JSON 数组
    printf("[");
    for (int j = 0; j < returnSize; j++) {
        if (j > 0) printf(",");
        printf("%d", res[j]);
    }
    printf("]\n");

    free(nums);
    free(res);
    return 0;
}
