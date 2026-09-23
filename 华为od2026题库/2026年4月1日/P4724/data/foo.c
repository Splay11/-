/**
 * @param target 目标目录路径
 * @param files 文件路径数组
 * @param filesSize 文件数量
 * @param sizes 文件大小数组
 * @param sizesSize 文件数量（与 filesSize 一致）
 * @param returnSize 输出参数，返回结果列表的大小
 * @return 占用空间最大的一级子项路径列表
 */
char** findMaxOccupiedPaths(char* target, char** files, int filesSize, int* sizes, int sizesSize, int* returnSize) {
    // 最大子项数不超过文件总数
    char** children = (char**)malloc(sizeof(char*) * filesSize);
    long long* occ = (long long*)malloc(sizeof(long long) * filesSize);
    int childCount = 0;

    int tlen = strlen(target);
    // 为防止末尾缺少'/'的判断，若target不是"/"且最后不是'/'则补一个'/'
    int needSlash = (strcmp(target, "/") != 0 && target[tlen - 1] != '/');
    char targetPrefix[256];
    strcpy(targetPrefix, target);
    if (needSlash) strcat(targetPrefix, "/");
    int plen = strlen(targetPrefix);
    int foundPrefix = 0;

    // 遍历每个文件
    for (int i = 0; i < filesSize; i++) {
        char* path = files[i];
        if (strncmp(path, targetPrefix, plen) == 0) {
            foundPrefix = 1;
            // 去掉target前缀后剩下的部分
            char* remain = path + plen;
            // 查找下一个'/'
            char* slash = strchr(remain, '/');
            char childPath[256];
            if (slash == NULL) {
                // 是一级文件
                sprintf(childPath, "%s%s", targetPrefix, remain);
                childPath[strlen(childPath) - 1 + (needSlash ? 0 : 0)]; //无操作仅防止警告
            } else {
                // 一级子目录
                int len = slash - remain;
                strncpy(childPath, targetPrefix, 255);
                strncat(childPath, remain, len);
                childPath[plen + len] = '\0';
                // 去掉最后多余的'/'
                if (childPath[strlen(childPath)-1] == '/')
                    childPath[strlen(childPath)-1] = '\0';
            }
            // 查找该子项是否已存在
            int idx = -1;
            for (int j = 0; j < childCount; j++) {
                if (strcmp(children[j], childPath) == 0) {
                    idx = j;
                    break;
                }
            }
            if (idx == -1) {
                children[childCount] = strdup(childPath);
                occ[childCount] = sizes[i];
                childCount++;
            } else {
                occ[idx] += sizes[i];
            }
        }
    }

    // 若不存在匹配前缀，返回空
    if (!foundPrefix) {
        *returnSize = 0;
        free(children);
        free(occ);
        return NULL;
    }

    // 找出最大占用空间
    long long maxv = -1;
    for (int i = 0; i < childCount; i++) {
        if (occ[i] > maxv) maxv = occ[i];
    }

    // 统计所有等于maxv的子项
    char** res = (char**)malloc(sizeof(char*) * childCount);
    int cnt = 0;
    for (int i = 0; i < childCount; i++) {
        if (occ[i] == maxv) {
            res[cnt++] = children[i];
        } else {
            free(children[i]);
        }
    }
    free(children);
    free(occ);

    // 按字典序排序
    for (int i = 0; i < cnt; i++) {
        for (int j = i + 1; j < cnt; j++) {
            if (strcmp(res[i], res[j]) > 0) {
                char* tmp = res[i];
                res[i] = res[j];
                res[j] = tmp;
            }
        }
    }

    *returnSize = cnt;
    return res;
}
