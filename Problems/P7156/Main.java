import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.util.StringTokenizer;

public class Main {
    // 环形加油站：总油不够则无解；否则扫一遍，油箱为负就改起点
    static int solve(int[] gas, int[] cost) {
        int n = gas.length;
        long total = 0;
        long tank = 0;
        int start = 0;
        for (int i = 0; i < n; i++) {
            // total 看整圈油是否够；tank 看当前起点走到 i 会不会没油
            long diff = (long) gas[i] - cost[i];
            total += diff;
            tank += diff;
            if (tank < 0) {
                // 从旧起点到 i 这段补不回来，只能从 i+1 重新出发
                start = i + 1;
                tank = 0;
            }
        }
        // 总油不够则任何起点都会失败；题目保证有解时起点唯一
        if (total < 0) {
            return -1;
        }
        return start;
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        StringTokenizer st = new StringTokenizer(br.readLine());
        int[] gas = new int[n];
        for (int i = 0; i < n; i++) {
            gas[i] = Integer.parseInt(st.nextToken());
        }
        st = new StringTokenizer(br.readLine());
        int[] cost = new int[n];
        for (int i = 0; i < n; i++) {
            cost[i] = Integer.parseInt(st.nextToken());
        }
        System.out.println(solve(gas, cost));
    }
}
