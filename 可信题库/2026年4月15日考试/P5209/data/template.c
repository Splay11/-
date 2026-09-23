#include "foo.c"
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int* parseArray1d(const char* s, int* outSize) {
    int cap = 16;
    int* vals = (int*)malloc((size_t)cap * sizeof(int));
    int n = 0;
    const char* p = s;
    while (*p && isspace((unsigned char)*p)) p++;
    if (*p != '[') exit(1);
    p++;
    while (1) {
        while (*p && isspace((unsigned char)*p)) p++;
        if (*p == ']') {
            p++;
            break;
        }
        int sign = 1;
        if (*p == '-') {
            sign = -1;
            p++;
        }
        if (!isdigit((unsigned char)*p)) exit(1);
        int v = 0;
        while (isdigit((unsigned char)*p)) {
            v = v * 10 + (*p - '0');
            p++;
        }
        if (n >= cap) {
            cap *= 2;
            vals = (int*)realloc(vals, (size_t)cap * sizeof(int));
        }
        vals[n++] = sign * v;
        while (*p && isspace((unsigned char)*p)) p++;
        if (*p == ']') {
            p++;
            break;
        }
        if (*p != ',') exit(1);
        p++;
    }
    *outSize = n;
    return vals;
}

int main(void) {
    char* line = (char*)malloc(1 << 20);
    if (!fgets(line, 1 << 20, stdin)) {
        free(line);
        return 0;
    }
    int numbersSize = 0;
    int* numbers = parseArray1d(line, &numbersSize);
    long long ans = sumOfSubarrayMedians(numbers, numbersSize);
    printf("%lld\n", ans);
    free(numbers);
    free(line);
    return 0;
}
