#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

// 用户函数声明
char** findMaxOccupiedPaths(const char* target,
                            char** files, int filesSize,
                            int* sizes, int sizesSize,
                            int* resultCount);

// 安全版 strdup
static char* my_strdup(const char* s) {
    size_t len = strlen(s);
    char* d = (char*)malloc(len + 1);
    if (d) {
        memcpy(d, s, len + 1);
    }
    return d;
}

// 读取全部 stdin 到动态缓冲区
static char* read_all(void) {
    size_t cap = 4096, len = 0;
    char* buf = (char*)malloc(cap);
    if (!buf) return NULL;
    int c;
    while ((c = getchar()) != EOF) {
        if (len + 1 >= cap) {
            cap *= 2;
            char* tmp = (char*)realloc(buf, cap);
            if (!tmp) { free(buf); return NULL; }
            buf = tmp;
        }
        buf[len++] = (char)c;
    }
    buf[len] = '\0';
    return buf;
}

// 跳过空白
static void skip_spaces(const char** p) {
    while (**p == ' ') (*p)++;
}

// 解析引号字符串
static char* parse_string(const char** p) {
    if (**p != '"') return NULL;
    (*p)++;
    const char* start = *p;
    while (**p && **p != '"') (*p)++;
    size_t len = *p - start;
    char* res = (char*)malloc(len + 1);
    if (res) {
        memcpy(res, start, len);
        res[len] = '\0';
    }
    if (**p == '"') (*p)++;
    return res;
}

// 解析字符串数组 ["a","b"]
static char** parse_str_array(const char** p, int* count) {
    if (**p != '[') return NULL;
    (*p)++;
    skip_spaces(p);
    int cap = 16;
    char** arr = (char**)malloc(cap * sizeof(char*));
    *count = 0;

    if (**p == ']') { (*p)++; return arr; }

    while (1) {
        skip_spaces(p);
        char* s = parse_string(p);
        if (!s) break;
        if (*count >= cap) {
            cap *= 2;
            arr = (char**)realloc(arr, cap * sizeof(char*));
        }
        arr[(*count)++] = s;
        skip_spaces(p);
        if (**p == ']') { (*p)++; break; }
        if (**p == ',') (*p)++;
    }
    return arr;
}

// 解析整数数组 [1,2,3]
static int* parse_int_array(const char** p, int* count) {
    if (**p != '[') return NULL;
    (*p)++;
    skip_spaces(p);
    int cap = 16;
    int* arr = (int*)malloc(cap * sizeof(int));
    *count = 0;

    if (**p == ']') { (*p)++; return arr; }

    while (1) {
        skip_spaces(p);
        int val = 0;
        bool neg = false;
        if (**p == '-') { neg = true; (*p)++; }
        while (**p >= '0' && **p <= '9') {
            val = val * 10 + (**p - '0');
            (*p)++;
        }
        if (neg) val = -val;
        if (*count >= cap) {
            cap *= 2;
            arr = (int*)realloc(arr, cap * sizeof(int));
        }
        arr[(*count)++] = val;
        skip_spaces(p);
        if (**p == ']') { (*p)++; break; }
        if (**p == ',') (*p)++;
    }
    return arr;
}

int main() {
    char* input = read_all();
    if (!input) return 1;

    // 去除尾部的 \r \n
    size_t len = strlen(input);
    while (len > 0 && (input[len - 1] == '\n' || input[len - 1] == '\r'))
        input[--len] = '\0';

    const char* p = input;

    // 解析 target
    char* target = parse_string(&p);

    // 跳过逗号和空白
    skip_spaces(&p);
    if (*p == ',') p++;

    // 解析 files
    skip_spaces(&p);
    int filesSize = 0;
    char** files = parse_str_array(&p, &filesSize);

    // 跳过逗号和空白
    skip_spaces(&p);
    if (*p == ',') p++;

    // 解析 sizes
    skip_spaces(&p);
    int sizesSize = 0;
    int* sizes = parse_int_array(&p, &sizesSize);

    // 调用用户函数
    int resultCount = 0;
    char** result = findMaxOccupiedPaths(target, files, filesSize,
                                          sizes, sizesSize, &resultCount);

    // 输出 JSON 数组
    printf("[");
    for (int i = 0; i < resultCount; i++) {
        if (i > 0) printf(", ");
        printf("\"%s\"", result[i]);
    }
    printf("]\n");

    // 释放内存
    free(target);
    for (int i = 0; i < filesSize; i++) free(files[i]);
    free(files);
    free(sizes);
    for (int i = 0; i < resultCount; i++) free(result[i]);
    free(result);
    free(input);

    return 0;
}
