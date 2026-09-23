import java.io.*;

public class Main {
    // 取 y = m/2 时对冲值最小：y XOR (m-y)
    static long minHedge(long m) {
        return (m / 2) ^ ((m + 1) / 2);
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < n; i++) {
            long m = Long.parseLong(br.readLine().trim());
            sb.append(minHedge(m)).append('\n');
        }
        System.out.print(sb);
    }
}
