#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#include "foo.c"

int main() {
    // 动态读取全部输入
    size_t cap = 1 << 20; // 1MB
    char* line = (char*)malloc(cap);
    size_t total = 0;
    while (1) {
        size_t r = fread(line + total, 1, cap - total - 1, stdin);
        if (r == 0) break;
        total += r;
        if (total + 1 >= cap) {
            cap *= 2;
            line = (char*)realloc(line, cap);
        }
    }
    line[total] = '\0';
    // 去除尾部换行
    while (total > 0 && (line[total - 1] == '\n' || line[total - 1] == '\r')) line[--total] = '\0';
    if (total == 0) {
        printf("\"-1\"\n");
        free(line);
        return 0;
    }
    // 格式检查: 必须以 { 开始，以 } 结束
    if (line[0] != '{' || line[total - 1] != '}') {
        printf("\"-1\"\n");
        free(line);
        return 0;
    }
    line[total - 1] = '\0';
    char *content = line + 1;

    // 构建链表（不在此处做值范围校验，交给 gameResult）
    struct ListNode* dummy = (struct ListNode*)malloc(sizeof(struct ListNode));
    struct ListNode* tail = dummy;
    dummy->next = NULL;
    char *tok = strtok(content, ",");
    while (tok) {
        while (*tok == ' ') tok++;
        if (*tok == '\0') {
            tok = strtok(NULL, ",");
            continue;
        }
        long long val = atoll(tok);
        struct ListNode* node = (struct ListNode*)malloc(sizeof(struct ListNode));
        node->val = (int)val;
        node->next = NULL;
        tail->next = node;
        tail = node;
        tok = strtok(NULL, ",");
    }
    struct ListNode* head = dummy->next;
    free(dummy);

    char* result = gameResult(head);
    printf("\"%s\"\n", result);

    struct ListNode* p = head;
    while (p) { struct ListNode* nxt = p->next; free(p); p = nxt; }
    free(result);
    free(line);
    return 0;
}
