import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.StringTokenizer;

public class Main {
    // 原位清空，不相邻同值不能并段，答案是极大等值段的段数
    static int countRuns(int[] xs) {
        if (xs.length == 0) {
            return 0;
        }
        int runs = 1;
        for (int i = 1; i < xs.length; i++) {
            // 和前一个工位零件个数不同，就要多勾一次
            if (xs[i] != xs[i - 1]) {
                runs++;
            }
        }
        return runs;
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int q = Integer.parseInt(br.readLine().trim());
        StringBuilder sb = new StringBuilder();
        for (int t = 0; t < q; t++) {
            StringTokenizer st = new StringTokenizer(br.readLine());
            int m = Integer.parseInt(st.nextToken());
            int[] xs = new int[m];
            for (int i = 0; i < m; i++) {
                xs[i] = Integer.parseInt(st.nextToken());
            }
            if (t > 0) {
                sb.append(' ');
            }
            sb.append(countRuns(xs));
        }
        // 同一行输出全部询问的最少勾取次数
        System.out.println(sb);
    }
}
