import java.util.Scanner;

// 枚举第二种操作次数；全体先按满击中算点名，再把豁免分到代价最小的位置
public class Main {
    public static void main(String[] args) {
        Scanner in = new Scanner(System.in);
        int n = in.nextInt();
        long heavy = in.nextLong();
        long light = in.nextLong();
        long[] load = new long[n];
        for (int i = 0; i < n; i++) {
            load[i] = in.nextLong();
        }
        in.close();
        System.out.println(minOps(load, heavy, light));
    }

    static long costWithType2(long[] load, long heavy, long light, long type2) {
        int n = load.length;
        long t0Sum = 0;
        long[] t0 = new long[n];
        long[] slack = new long[n];
        for (int i = 0; i < n; i++) {
            long x = load[i];
            // 先假设每个数都被第二种操作打中 type2 次
            long rest = x - light * type2;
            if (rest > 0) {
                long need = (rest + heavy - 1) / heavy;
                t0Sum += need;
                t0[i] = need;
                slack[i] = 0;
            } else {
                t0[i] = 0;
                if (x <= 0) {
                    slack[i] = type2;
                } else {
                    long needB = (x + light - 1) / light;
                    slack[i] = Math.max(0L, type2 - needB);
                }
            }
        }
        // 第二种操作必须选中某几个下标共 type2 次，这些下标当次不会被减 B
        long free = 0;
        for (int i = 0; i < n; i++) {
            free += slack[i];
        }
        if (free >= type2) {
            return type2 + t0Sum;
        }
        long extra = type2 - free;
        long bestDelta = -1;
        for (int i = 0; i < n; i++) {
            long used = slack[i] + extra;
            if (used > type2) {
                continue;
            }
            long hits = type2 - used;
            long rest = load[i] - light * hits;
            long need = rest <= 0 ? 0 : (rest + heavy - 1) / heavy;
            long delta = need - t0[i];
            if (bestDelta < 0 || delta < bestDelta) {
                bestDelta = delta;
            }
        }
        if (bestDelta < 0) {
            return Long.MAX_VALUE / 4;
        }
        return type2 + t0Sum + bestDelta;
    }

    static long minOps(long[] load, long heavy, long light) {
        int n = load.length;
        long onlyA = 0;
        for (int i = 0; i < n; i++) {
            if (load[i] > 0) {
                onlyA += (load[i] + heavy - 1) / heavy;
            }
        }
        if (n == 1) {
            return onlyA;
        }
        long maxNeed = 0;
        long sumNeed = 0;
        for (int i = 0; i < n; i++) {
            long needB = 0;
            if (load[i] > 0) {
                needB = (load[i] + light - 1) / light;
            }
            if (needB > maxNeed) {
                maxNeed = needB;
            }
            sumNeed += needB;
        }
        long maxS = Math.max(maxNeed, (sumNeed + n - 2) / (n - 1));
        long best = onlyA;
        // S 再大也比只减 A 更亏
        if (maxS > onlyA) {
            maxS = onlyA;
        }
        for (long type2 = 0; type2 <= maxS; type2++) {
            long cur = costWithType2(load, heavy, light, type2);
            if (cur < best) {
                best = cur;
            }
        }
        return best;
    }
}
