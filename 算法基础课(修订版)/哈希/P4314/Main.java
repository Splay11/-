import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        String s = br.readLine().trim();

        long[] freq = new long[26];
        long tot = 0, wrap = 0;
        StringBuilder sb = new StringBuilder();

        for (int i = 1; i <= n; i++) {
            tot += i;
            int k = s.charAt(i - 1) - 'a';
            wrap += freq[k] + 1;  // 增量 f+1
            freq[k]++;
            sb.append(tot - wrap).append("\n");
        }

        System.out.print(sb.toString());
    }
}
