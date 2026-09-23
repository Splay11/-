#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// 前置声明用户函数
char* lightStripTransform(char* lights, int t);

int main() {
    char line[4096];
    fgets(line, sizeof(line), stdin);
    int len = strlen(line);
    while (len > 0 && (line[len - 1] == '\n' || line[len - 1] == '\r'))
        line[--len] = '\0';

    // 解析输入："lights",t
    // 找到第一个引号后的内容
    char* start = strchr(line, '"');
    char* end = strchr(start + 1, '"');
    int lightsLen = (int)(end - start - 1);
    char lights[17];
    strncpy(lights, start + 1, lightsLen);
    lights[lightsLen] = '\0';

    // 逗号后的整数
    char* comma = strchr(end, ',');
    int t = atoi(comma + 1);

    char* result = lightStripTransform(lights, t);
    printf("\"%s\"\n", result);
    free(result);
    return 0;
}
