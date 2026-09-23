import java.util.Scanner;

public class Main {
    static int[] farthestPosts(String[] grid) {
        // 曼哈顿距离 |r1-r2|+|c1-c2| 等于 max(|(r+c)之差|, |(r-c)之差|)
        // 扫一遍过道，记下两类极值点，取较差更大的那一对
        int inf = 1000000000;
        int minS = inf, maxS = -inf;
        int minD = inf, maxD = -inf;
        int psR = 0, psC = 0, qsR = 0, qsC = 0;
        int pdR = 0, pdC = 0, qdR = 0, qdC = 0;
        for (int i = 0; i < grid.length; i++) {
            String row = grid[i];
            for (int j = 0; j < row.length(); j++) {
                if (row.charAt(j) != '.') {
                    continue;
                }
                int r = i + 1;
                int c = j + 1;
                int s = r + c;
                int d = r - c;
                if (s < minS) {
                    minS = s;
                    psR = r;
                    psC = c;
                }
                if (s > maxS) {
                    maxS = s;
                    qsR = r;
                    qsC = c;
                }
                if (d < minD) {
                    minD = d;
                    pdR = r;
                    pdC = c;
                }
                if (d > maxD) {
                    maxD = d;
                    qdR = r;
                    qdC = c;
                }
            }
        }
        // r+c 全相同则两个和值点重合，必须改用 r-c
        int[] ans = new int[4];
        if ((psR != qsR || psC != qsC) && maxS - minS >= maxD - minD) {
            ans[0] = psR;
            ans[1] = psC;
            ans[2] = qsR;
            ans[3] = qsC;
        } else {
            ans[0] = pdR;
            ans[1] = pdC;
            ans[2] = qdR;
            ans[3] = qdC;
        }
        return ans;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int h = sc.nextInt();
        int w = sc.nextInt();
        String[] grid = new String[h];
        for (int i = 0; i < h; i++) {
            grid[i] = sc.next();
        }
        int[] ans = farthestPosts(grid);
        System.out.println(ans[0] + " " + ans[1] + " " + ans[2] + " " + ans[3]);
        sc.close();
    }
}
