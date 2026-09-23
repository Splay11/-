#include <stdlib.h>
#include <string.h>

int** countKeys(char* s, int* returnSize) {
    int cnt[36] = {0};  // 0-9: digits, 10-35: a-z
    int n = strlen(s);
    int i = 0;

    // 解析按键
    while (i < n) {
        if (i + 1 < n && s[i] == 'u' && s[i + 1] == 'u') {
            // uu → j (encoded as 19)
            cnt[19]++;
            i += 2;
        } else if (i + 1 < n && s[i] == 't' && s[i + 1] == 't') {
            // tt → b (encoded as 11)
            cnt[11]++;
            i += 2;
        } else {
            // 普通按键
            char c = s[i];
            int enc;
            if (c >= '0' && c <= '9') {
                enc = c - '0';
            } else {
                enc = c - 'a' + 10;
            }
            cnt[enc]++;
            i++;
        }
    }

    // 统计有效按键数
    int num = 0;
    for (int k = 0; k < 36; k++) {
        if (cnt[k] > 0) num++;
    }

    // 分配结果数组
    int** res = (int**)malloc(num * sizeof(int*));
    int idx = 0;
    // 按次数降序，同次数按键值升序
    for (int freq = 500; freq >= 1; freq--) {
        for (int k = 0; k < 36; k++) {
            if (cnt[k] == freq) {
                res[idx] = (int*)malloc(2 * sizeof(int));
                res[idx][0] = k;
                res[idx][1] = freq;
                idx++;
            }
        }
    }

    *returnSize = num;
    return res;
}
