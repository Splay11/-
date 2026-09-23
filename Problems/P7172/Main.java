import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.util.StringTokenizer;

public class Main {
    // 按题面公式：最高位符号位贡献 -2^(n-1)，其余位按正权
    static int solve(int[] bits) {
        int n = bits.length;
        int ans = 0;
        if (bits[0] == 1) {
            ans -= (1 << (n - 1));
        }
        for (int i = 1; i < n; i++) {
            if (bits[i] == 1) {
                ans += (1 << (n - 1 - i));
            }
        }
        return ans;
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        StringTokenizer st = new StringTokenizer(br.readLine());
        int[] bits = new int[n];
        for (int i = 0; i < n; i++) {
            bits[i] = Integer.parseInt(st.nextToken());
        }
        System.out.println(solve(bits));
    }
}
