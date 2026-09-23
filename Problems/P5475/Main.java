import java.util.Arrays;
import java.util.Comparator;
import java.util.Scanner;

// 按分数升序赋平均名次，再用 Mann-Whitney U 还原 AUC
public class Main {
    public static void main(String[] args) {
        Scanner in = new Scanner(System.in);
        // 四级协议：第一行笔数，第二行标签，第三行风险分
        int m = in.nextInt();
        int[] labels = new int[m];
        double[] scores = new double[m];
        for (int i = 0; i < m; i++) {
            labels[i] = in.nextInt();
        }
        for (int i = 0; i < m; i++) {
            scores[i] = in.nextDouble();
        }
        in.close();
        System.out.printf("%.6f\n", aucFromRanks(labels, scores));
    }

    static double aucFromRanks(int[] labels, double[] scores) {
        int m = labels.length;
        Integer[] order = new Integer[m];
        for (int i = 0; i < m; i++) {
            order[i] = i;
        }
        // 按下标稳定排序，保证同分时相对顺序确定
        final double[] sc = scores;
        Arrays.sort(order, new Comparator<Integer>() {
            public int compare(Integer a, Integer b) {
                if (sc[a] != sc[b]) {
                    return sc[a] < sc[b] ? -1 : 1;
                }
                return a.intValue() - b.intValue();
            }
        });
        double[] rank = new double[m];
        int i = 0;
        while (i < m) {
            int j = i;
            // 向右扩到同一分数的最后一笔
            while (j + 1 < m && sc[order[j + 1]] == sc[order[i]]) {
                j++;
            }
            // 名次从 1 起，区间 [i+1, j+1]
            double avg = (i + 1 + j + 1) / 2.0;
            for (int k = i; k <= j; k++) {
                rank[order[k]] = avg;
            }
            i = j + 1;
        }
        int kPos = 0;
        double sPos = 0.0;
        for (int t = 0; t < m; t++) {
            if (labels[t] == 1) {
                kPos++;
                sPos += rank[t];
            }
        }
        int kNeg = m - kPos;
        // U 统计量：正类名次和减去「全排在最前」时的最小名次和
        double u = sPos - kPos * (kPos + 1) / 2.0;
        return u / (kPos * kNeg);
    }
}
