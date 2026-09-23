import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] sp = br.readLine().trim().split("\\s+");
        int n = Integer.parseInt(sp[0]);
        long k = Long.parseLong(sp[1]);
        sp = br.readLine().trim().split("\\s+");

        Map<Long, Long> cnt = new HashMap<>();
        cnt.put(0L, 1L);  // 空前缀
        long pref = 0, ans = 0;
        for (int i = 0; i < n; i++) {
            long x = Long.parseLong(sp[i]);
            pref ^= x;
            // 需要之前前缀异或为 pref^k
            ans += cnt.getOrDefault(pref ^ k, 0L);
            cnt.put(pref, cnt.getOrDefault(pref, 0L) + 1);
        }
        System.out.println(ans);
    }
}
