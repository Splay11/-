import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.Scanner;

// 按当前波次的标签增量贪心挑主机；增量打平时取更小的 nid
public class Main {
    public static void main(String[] args) {
        Scanner in = new Scanner(System.in);
        int p = in.nextInt();
        int d = in.nextInt();
        int[] nid = new int[p];
        String[][] tags = new String[p][d];
        for (int i = 0; i < p; i++) {
            nid[i] = in.nextInt();
            for (int j = 0; j < d; j++) {
                tags[i][j] = in.next();
            }
        }
        int b = in.nextInt();
        in.close();

        int[][] waves = assignBatches(nid, tags, d, b);
        for (int w = 0; w < waves.length; w++) {
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < waves[w].length; i++) {
                if (i > 0) {
                    sb.append(' ');
                }
                sb.append(waves[w][i]);
            }
            System.out.println(sb.toString());
        }
    }

    // 按题面规则把主机分进 b 个波次，每个波次内 nid 已升序
    static int[][] assignBatches(int[] nid, String[][] tags, int d, int b) {
        int p = nid.length;
        // 前 (b-r) 波容量 q，最后 r 波容量 q+1
        int base = p / b;
        int extra = p % b;
        int[] sizes = new int[b];
        for (int i = 0; i < b - extra; i++) {
            sizes[i] = base;
        }
        for (int i = 0; i < extra; i++) {
            sizes[b - extra + i] = base + 1;
        }

        boolean[] used = new boolean[p];
        int[][] result = new int[b][];
        for (int w = 0; w < b; w++) {
            int cap = sizes[w];
            int[] wave = new int[cap];
            // 每个维度各自维护「本波次已出现过的标签」
            ArrayList<HashSet<String>> seen = new ArrayList<HashSet<String>>();
            for (int j = 0; j < d; j++) {
                seen.add(new HashSet<String>());
            }
            for (int t = 0; t < cap; t++) {
                int bestInc = -1;
                int bestPos = -1;
                for (int i = 0; i < p; i++) {
                    if (used[i]) {
                        continue;
                    }
                    // 增量：该机各维标签里，本波次还没出现过的个数
                    int inc = 0;
                    for (int j = 0; j < d; j++) {
                        if (!seen.get(j).contains(tags[i][j])) {
                            inc++;
                        }
                    }
                    // 增量更大优先；打平则 nid 更小优先
                    if (inc > bestInc ||
                            (inc == bestInc && (bestPos == -1 || nid[i] < nid[bestPos]))) {
                        bestInc = inc;
                        bestPos = i;
                    }
                }
                used[bestPos] = true;
                wave[t] = nid[bestPos];
                for (int j = 0; j < d; j++) {
                    seen.get(j).add(tags[bestPos][j]);
                }
            }
            Arrays.sort(wave);
            result[w] = wave;
        }
        return result;
    }
}
