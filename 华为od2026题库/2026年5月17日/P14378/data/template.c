#include "foo.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#define MAX_LEN 100000

int main() {
    char line[MAX_LEN];
    if (!fgets(line, MAX_LEN, stdin)) return 0;
    int len = strlen(line);
    while (len > 0 && (line[len - 1] == '\n' || line[len - 1] == '\r')) line[--len] = '\0';

    char preorderStr[MAX_LEN] = {0};
    char inorderStr[MAX_LEN] = {0};
    char beDeletedNode[MAX_LEN] = {0};

    // expected format:  "ABC","BAC",A
    // parse by commas outside quotes
    int stage = 0, idx1 = 0, idx2 = 0, idx3 = 0;
    bool inQuote = false;
    for (int i = 0; i < len; i++) {
        char c = line[i];
        if (c == '"') {
            inQuote = !inQuote;
            continue;
        }
        if (!inQuote && c == ',') {
            stage++;
            continue;
        }
        if (stage == 0) {
            preorderStr[idx1++] = c;
        } else if (stage == 1) {
            inorderStr[idx2++] = c;
        } else if (stage == 2) {
            beDeletedNode[idx3++] = c;
        }
    }
    preorderStr[idx1] = '\0';
    inorderStr[idx2] = '\0';
    beDeletedNode[idx3] = '\0';

    // trim spaces
    for(int i=0;i<idx3;i++){
        if(beDeletedNode[i]==' '){
            memmove(beDeletedNode+i, beDeletedNode+i+1, strlen(beDeletedNode+i));
            i--;
        }
    }

    char* result = buildAfterDelete(preorderStr, inorderStr, beDeletedNode);
    printf("\"%s\"\n", result);
    free(result);
    return 0;
}
