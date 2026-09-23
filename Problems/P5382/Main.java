import java.util.Scanner;

public class Main {
    // 沿当前方向扫描，能揭就揭；整趟没有进展则失败，否则掉头继续
    static int minTurns(int[] w) {
        int n = w.length;
        boolean[] opened = new boolean[n];
        int keys = 0;
        int done = 0;
        int ans = 0;
        int d = 1;
        int i = 0;
        while (done < n) {
            int gained = 0;
            // 沿当前方向走到尽头，路过能揭的彩门就揭
            while (i >= 0 && i < n) {
                if (!opened[i] && keys >= w[i]) {
                    opened[i] = true;
                    keys++;
                    done++;
                    gained++;
                }
                i += d;
            }
            if (done == n) {
                return ans;
            }
            // 这一趟一扇都没揭开，剩下的阈值永远够不着
            if (gained == 0) {
                return -1;
            }
            // 走到尽头后换向，从端点外再踏回数组
            d = -d;
            i += d;
            ans++;
        }
        return ans;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int q = sc.nextInt();
        for (int t = 0; t < q; t++) {
            int m = sc.nextInt();
            int[] w = new int[m];
            for (int j = 0; j < m; j++) {
                w[j] = sc.nextInt();
            }
            System.out.println(minTurns(w));
        }
        sc.close();
    }
}
