import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int q = Integer.parseInt(br.readLine().trim());
        StringBuilder sb = new StringBuilder();
        while (q-- > 0) {
            StringTokenizer st = new StringTokenizer(br.readLine());
            int m = Integer.parseInt(st.nextToken());
            long t = Long.parseLong(st.nextToken());
            ArrayList<Integer> out = new ArrayList<>();
            int s = m;
            while (s >= 1) {
                if (t >= s - 1 && s > 1) {
                    out.add(s); // 放最大值
                    t -= (s - 1);
                    s--;
                } else {
                    if (t == 0) {
                        for (int i = 1; i <= s; i++) out.add(i);
                    } else {
                        out.add((int) t + 1);
                        for (int i = 1; i <= t; i++) out.add(i);
                        for (int i = (int) t + 2; i <= s; i++) out.add(i);
                    }
                    break;
                }
            }
            for (int i = 0; i < out.size(); i++) {
                if (i > 0) sb.append(' ');
                sb.append(out.get(i));
            }
            sb.append('\n');
        }
        System.out.print(sb);
    }
}
