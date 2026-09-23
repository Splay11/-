import java.util.Scanner;

// 二分消费轮次：每轮全体减 q，被点中的再多减 p-q
public class Main {
    public static void main(String[] args) {
        Scanner in = new Scanner(System.in);
        // 四级协议：第一行主题数，第二行 p q，第三行全部积压
        int m = in.nextInt();
        long p = in.nextLong();
        long q = in.nextLong();
        long[] w = new long[m];
        for (int i = 0; i < m; i++) {
            w[i] = in.nextLong();
        }
        in.close();
        System.out.println(minStarts(w, p, q));
    }

    // times 轮是否够把所有积压清到不超过 0
    static boolean enough(long times, long[] heat, long center, long ambient) {
        long extra = center - ambient;
        long need = 0;
        // 先按顺带消费 times 轮，剩下的必须靠主消费补
        long cooled = ambient * times;
        for (int i = 0; i < heat.length; i++) {
            long rest = heat[i] - cooled;
            if (rest > 0) {
                // 向上取整：还要做主消费多少轮
                need += (rest + extra - 1) / extra;
                if (need > times) {
                    return false;
                }
            }
        }
        return true;
    }

    static long minStarts(long[] heat, long center, long ambient) {
        long lo = 0;
        long hi = 0;
        for (int i = 0; i < heat.length; i++) {
            long w = heat[i];
            // 就算每轮都点它，也至少要 ceil(w/p) 轮
            long needCenter = (w + center - 1) / center;
            if (needCenter > lo) {
                lo = needCenter;
            }
            // 从不点它、只吃顺带消费，ceil(w/q) 轮一定够
            long needAmb = (w + ambient - 1) / ambient;
            if (needAmb > hi) {
                hi = needAmb;
            }
        }
        while (lo < hi) {
            long mid = (lo + hi) / 2;
            if (enough(mid, heat, center, ambient)) {
                hi = mid;
            } else {
                lo = mid + 1;
            }
        }
        return lo;
    }
}
