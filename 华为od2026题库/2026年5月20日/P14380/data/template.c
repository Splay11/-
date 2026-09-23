#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

int equalDistanceBinary(int n);

int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    int result = equalDistanceBinary(n);
    printf("%d\n", result);
    return 0;
}
