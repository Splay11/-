import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.StringTokenizer;

public class Main {
    static final double EPS = 1e-6;

    // 四个数做 24 点：每次取两个数做四则运算再递归
    static boolean dfs(ArrayList<Double> a) {
        if (a.size() == 1) {
            return Math.abs(a.get(0) - 24.0) < EPS;
        }
        int n = a.size();
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                if (i == j) {
                    continue;
                }
                ArrayList<Double> rest = new ArrayList<Double>();
                for (int k = 0; k < n; k++) {
                    if (k != i && k != j) {
                        rest.add(a.get(k));
                    }
                }
                double x = a.get(i);
                double y = a.get(j);
                double[] cands = new double[4];
                int m = 3;
                cands[0] = x + y;
                cands[1] = x - y;
                cands[2] = x * y;
                if (Math.abs(y) > EPS) {
                    cands[3] = x / y;
                    m = 4;
                }
                for (int t = 0; t < m; t++) {
                    ArrayList<Double> nxt = new ArrayList<Double>(rest);
                    nxt.add(cands[t]);
                    if (dfs(nxt)) {
                        return true;
                    }
                }
            }
        }
        return false;
    }

    static boolean solve(int[] cards) {
        ArrayList<Double> a = new ArrayList<Double>();
        for (int i = 0; i < 4; i++) {
            a.add((double) cards[i]);
        }
        return dfs(a);
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st = new StringTokenizer(br.readLine());
        int[] cards = new int[4];
        for (int i = 0; i < 4; i++) {
            cards[i] = Integer.parseInt(st.nextToken());
        }
        System.out.println(solve(cards) ? "true" : "false");
    }
}
