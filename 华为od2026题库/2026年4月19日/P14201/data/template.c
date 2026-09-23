#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

int processInstructions(char* instructions);

int main() {
    char instructions[1024];
    int result = 0;
    if (fgets(instructions, sizeof(instructions), stdin) != NULL) {
        int len = strlen(instructions);
        while (len > 0 && (instructions[len - 1] == '\n' || instructions[len - 1] == '\r'))
            instructions[--len] = '\0';
        result = processInstructions(instructions);
    }
    printf("%d\n", result);
    return 0;
}
