#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int maxDepth(char** nodes, int nodesSize) {
    // 空树或根节点为空
    if (nodesSize == 0 || strcmp(nodes[0], "#") == 0) {
        return 0;
    }

    // 队列存储深度（最多 1024 个节点）
    int queue[1100];
    int head = 0, tail = 0;

    // 根节点深度为 1
    queue[tail++] = 1;
    int ans = 1;
    int index = 1;  // 下一个要处理的子节点下标

    while (head < tail) {
        int depth = queue[head++];

        // 处理左子节点
        if (index < nodesSize) {
            if (strcmp(nodes[index], "#") != 0) {
                queue[tail++] = depth + 1;
                if (depth + 1 > ans) ans = depth + 1;
            }
            index++;
        }

        // 处理右子节点
        if (index < nodesSize) {
            if (strcmp(nodes[index], "#") != 0) {
                queue[tail++] = depth + 1;
                if (depth + 1 > ans) ans = depth + 1;
            }
            index++;
        }
    }

    return ans;
}
