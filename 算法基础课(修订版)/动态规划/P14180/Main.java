import java.util.Arrays;
import java.util.Scanner;

public class Main {
    static int n;
    static int[] dp;
    static Box[] box;

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        n = sc.nextInt();
        box = new Box[n + 1];
        dp = new int[n + 1];

        for (int i = 1; i <= n; i++) {
            box[i] = new Box(sc.nextInt(), sc.nextInt(), sc.nextInt());
        }

        Arrays.sort(box, 1, n + 1, (a, b) -> {
            if (a.l != b.l) {
                return a.l - b.l;
            }
            if (a.w != b.w) {
                return a.w - b.w;
            }
            return a.h - b.h;
        });

        int ans = 0;
        for (int i = 1; i <= n; i++) {
            dp[i] = box[i].h;
            for (int j = 1; j < i; j++) {
                if (box[i].h > box[j].h && box[i].l > box[j].l && box[i].w > box[j].w) {
                    dp[i] = Math.max(dp[i], dp[j] + box[i].h);
                }
            }
            ans = Math.max(ans, dp[i]);
        }
        System.out.println(ans);
        sc.close();
    }

    static class Box {
        int l, w, h;

        Box(int l, int w, int h) {
            this.l = l;
            this.w = w;
            this.h = h;
        }
    }
}
