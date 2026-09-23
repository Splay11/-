import java.util.*;
import java.io.*;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        PrintWriter out = new PrintWriter(new BufferedOutputStream(System.out));

        int T = Integer.parseInt(br.readLine());
        while (T-- > 0) {
            StringTokenizer st = new StringTokenizer(br.readLine());
            long a = Long.parseLong(st.nextToken());  // 初始值
            long b = Long.parseLong(st.nextToken());  // 目标值
            long diff = b - a;                         // 需增加的值
            int ans = Long.bitCount(diff);             // bitCount 等价于 popcount
            out.println(ans);
        }
        out.flush();
    }
}
