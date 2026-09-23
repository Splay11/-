import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    // 灯位从 1 开始：奇数位放 0，偶数位放 1，得到 0101...
    static String buildBalanced01(int k) {
        StringBuilder sb = new StringBuilder(k);
        for (int i = 1; i <= k; i++) {
            if (i % 2 == 1) {
                sb.append('0');
            } else {
                sb.append('1');
            }
        }
        return sb.toString();
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        // 第一行灯带长度，第二行窗口条数
        int k = Integer.parseInt(br.readLine().trim());
        int q = Integer.parseInt(br.readLine().trim());
        // 窗口写成 a,b，交错串对所有窗口都成立，读掉即可
        for (int i = 0; i < q; i++) {
            br.readLine();
        }
        System.out.println(buildBalanced01(k));
    }
}
