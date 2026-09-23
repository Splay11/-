#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>

// 最大字符串长度
#define MAX_LEN 100000
#define MAX_NUMS 1000

// 解析整型列表 "[a,b,c,...]"
// 返回动态分配的 int 数组，*outCount 存储元素个数
static int* parseIntList(const char* s, int* outCount) {
    int* res = (int*)malloc(MAX_NUMS * sizeof(int));
    *outCount = 0;
    int i = 1;  // 跳过 '['
    int n = (int)strlen(s);
    while (i < n) {
        // 跳过空格
        while (i < n && s[i] == ' ') i++;
        if (i >= n || s[i] == ']') break;
        int sign = 1;
        if (s[i] == '-') { sign = -1; i++; }
        int num = 0;
        while (i < n && isdigit((unsigned char)s[i])) {
            num = num * 10 + (s[i] - '0');
            i++;
        }
        res[*outCount] = sign * num;
        (*outCount)++;
        // 跳过逗号
        if (i < n && s[i] == ',') i++;
    }
    return res;
}

// 查找顶层逗号（不在括号内的逗号）
static int findTopLevelComma(const char* s) {
    int bracket = 0;
    int len = (int)strlen(s);
    for (int i = 0; i < len; i++) {
        char c = s[i];
        if (c == '[') bracket++;
        else if (c == ']') bracket--;
        else if (c == ',' && bracket == 0) return i;
    }
    return -1;
}

// 前向声明
int maxMushroomValue(int count, int total,
                     int* values, int valuesSize,
                     int* decays, int decaysSize);

int main() {
    char line[MAX_LEN];
    fgets(line, MAX_LEN, stdin);
    int len = (int)strlen(line);
    // 去除末尾换行符
    while (len > 0 && (line[len - 1] == '\n' || line[len - 1] == '\r'))
        line[--len] = '\0';

    // 解析 count
    int comma1 = findTopLevelComma(line);
    char countStr[16];
    strncpy(countStr, line, comma1);
    countStr[comma1] = '\0';
    int count = atoi(countStr);

    // 解析 total
    const char* rest1 = line + comma1 + 1;
    int comma2 = findTopLevelComma(rest1);
    char totalStr[16];
    strncpy(totalStr, rest1, comma2);
    totalStr[comma2] = '\0';
    int total = atoi(totalStr);

    // 解析数组部分
    const char* rest2 = rest1 + comma2 + 1;
    const char* split = strstr(rest2, "],[");
    int splitPos = (int)(split - rest2);

    // values 数组
    char* valuesStr = (char*)malloc(splitPos + 2);
    strncpy(valuesStr, rest2, splitPos + 1);
    valuesStr[splitPos + 1] = '\0';

    // decays 数组：需要加上 '[' 前缀
    const char* decaysStrSuffix = rest2 + splitPos + 3;
    int suffixLen = (int)strlen(decaysStrSuffix);
    char* decaysStr = (char*)malloc(suffixLen + 3);
    decaysStr[0] = '[';
    strcpy(decaysStr + 1, decaysStrSuffix);

    int valuesSize = 0, decaysSize = 0;
    int* values = parseIntList(valuesStr, &valuesSize);
    int* decays = parseIntList(decaysStr, &decaysSize);

    int result = maxMushroomValue(count, total,
                                  values, valuesSize,
                                  decays, decaysSize);
    printf("%d\n", result);

    free(valuesStr);
    free(decaysStr);
    free(values);
    free(decays);

    return 0;
}
