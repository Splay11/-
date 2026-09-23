import java.util.HashMap;
import java.util.Map;
import java.util.Scanner;

public class Main {
    static boolean canFinish(int c, long q, long w, long[] h, long[][] freq, long days) {
        // 判定：在 days 天内能不能打掉 q 块矿岩
        if (days <= 0) {
            return false;
        }
        // days = full 个完整周期 + 多出来的 rest 天
        long full = days / c;
        int rest = (int) (days % c);
        long done = 0;
        for (int t = 0; t < freq.length; t++) {
            long x = freq[t][0];
            long cnt = freq[t][1];
            long add;
            if (x <= w) {
                // 初始功率已经够打这个硬度，每个完整周期都能打一次
                add = full;
            } else {
                // 完整周期里功率依次是 w, w+1, ..., w+full-1
                // 要功率 >= x，需要过完 x-w 个周期之后才开始贡献
                add = full - (x - w);
                if (add < 0) {
                    add = 0;
                }
            }
            if (add == 0) {
                continue;
            }
            // add * cnt 可能很大，先判断是否已经够 q 块，避免撑爆 long
            if (add >= q || cnt >= q || add > (q - 1) / cnt) {
                return true;
            }
            done += add * cnt;
            if (done >= q) {
                return true;
            }
        }
        // 多出来的 rest 天功率固定为 w+full，对应周期前 rest 个位置
        long atk = w + full;
        for (int i = 0; i < rest; i++) {
            if (h[i] <= atk) {
                done++;
                if (done >= q) {
                    return true;
                }
            }
        }
        return done >= q;
    }

    static long[][] buildFreq(long[] h) {
        // 相同硬度合并，二分时只扫不同的硬度值
        HashMap<Long, Integer> mp = new HashMap<Long, Integer>();
        for (int i = 0; i < h.length; i++) {
            Integer old = mp.get(h[i]);
            if (old == null) {
                mp.put(h[i], 1);
            } else {
                mp.put(h[i], old + 1);
            }
        }
        long[][] freq = new long[mp.size()][2];
        int p = 0;
        for (Map.Entry<Long, Integer> e : mp.entrySet()) {
            freq[p][0] = e.getKey();
            freq[p][1] = e.getValue();
            p++;
        }
        return freq;
    }

    static long minDays(int c, long q, long w, long[] h) {
        long[][] freq = buildFreq(h);
        // 天数越多越容易打完，对天数二分找最小可行值
        long lo = 1, hi = 4000000000000000000L, ans = 4000000000000000000L;
        while (lo <= hi) {
            long mid = lo + (hi - lo) / 2;
            if (canFinish(c, q, w, h, freq, mid)) {
                ans = mid;
                hi = mid - 1;
            } else {
                lo = mid + 1;
            }
        }
        return ans;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int c = sc.nextInt();
        long q = sc.nextLong();
        long w = sc.nextLong();
        long[] h = new long[c];
        for (int i = 0; i < c; i++) {
            h[i] = sc.nextLong();
        }
        System.out.println(minDays(c, q, w, h));
        sc.close();
    }
}
