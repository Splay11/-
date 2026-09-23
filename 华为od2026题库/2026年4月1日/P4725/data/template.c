#include "foo.c"
#include <stdio.h>

// 用户函数声明
int getNthValue(int M, int N);

int main() {
    int M, N;
    scanf("%d,%d", &M, &N);
    int result = getNthValue(M, N);
    printf("%d\n", result);
    return 0;
}
