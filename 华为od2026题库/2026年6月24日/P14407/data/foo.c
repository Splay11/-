#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <stdbool.h>

// 按时间段交集比例计算加权贡献
static double weighted(long long amount, long long start, long long end,
                        long long qs, long long qe) {
    if (start > qe || end < qs) return 0.0;
    long long duration = end - start;
    if (duration == 0) {
        if (qs <= start && start <= qe) return (double)amount;
        return 0.0;
    }
    long long os = start > qs ? start : qs;
    long long oe = end < qe ? end : qe;
    if (os > oe) return 0.0;
    long long overlap = oe - os;
    return (double)amount * (double)overlap / (double)duration;
}

// 四舍五入并夹到 int32 范围
static int roundToI32(double x) {
    long long val = x >= 0 ? (long long)floor(x + 0.5) : (long long)ceil(x - 0.5);
    if (val > 2147483647LL) return 2147483647;
    if (val < -2147483648LL) return -2147483648;
    return (int)val;
}

// 按单字符分隔符 split 字符串（兼容 — 不依赖 strtok）
static int split(char* s, char delim, char** parts, int maxParts) {
    int cnt = 0;
    char* start = s;
    for (int i = 0; ; i++) {
        if (s[i] == delim || s[i] == '\0') {
            parts[cnt++] = start;
            if (cnt >= maxParts || s[i] == '\0') break;
            s[i] = '\0';
            start = s + i + 1;
        }
    }
    return cnt;
}

int queryNetEnergy(char** commands, int commandsSize) {
    // 解析最后一条查询命令
    char* query = commands[commandsSize - 1];
    char* qparts[5];
    int qcnt = split(query, ',', qparts, 5);
    // qparts[0] = "QueryNetEnergy", qparts[1] = version/A, qparts[2]=qs, qparts[3]=qe
    bool useAll = strcmp(qparts[1], "A") == 0;
    long long qs = atoll(qparts[2]);
    long long qe = atoll(qparts[3]);
    int maxVersion = useAll ? 1000000000 : atoi(qparts[1]);

    double total = 0.0;
    int version = 0;
    for (int i = 0; i < commandsSize - 1; i++) {
        version++;
        if (version > maxVersion) break;

        char* parts[5];
        int pcnt = split(commands[i], ',', parts, 5);

        if (strcmp(parts[0], "AddProductionRecord") == 0) {
            // AddProductionRecord,type,amount,start,end
            long long amount = atoll(parts[2]);
            long long start = atoll(parts[3]);
            long long end   = atoll(parts[4]);
            total += weighted(amount, start, end, qs, qe);
        } else if (strcmp(parts[0], "AddConsumptionRecord") == 0) {
            // AddConsumptionRecord,amount,start,end
            long long amount = atoll(parts[1]);
            long long start = atoll(parts[2]);
            long long end   = atoll(parts[3]);
            total -= weighted(amount, start, end, qs, qe);
        }
    }

    return roundToI32(total);
}
