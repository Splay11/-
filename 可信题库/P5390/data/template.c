#include "foo.c"
#include <stdio.h>
#include <string.h>

#define MAX_LEN 2000005

static char buf[MAX_LEN];

int main(void) {
    if (!fgets(buf, MAX_LEN, stdin)) return 0;
    size_t n = strlen(buf);
    while (n > 0 && (buf[n - 1] == '\n' || buf[n - 1] == '\r')) buf[--n] = '\0';
    printf("%s\n", reviseMarks(buf));
    return 0;
}
