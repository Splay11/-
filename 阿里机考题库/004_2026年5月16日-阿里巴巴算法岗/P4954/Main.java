import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st = new StringTokenizer(br.readLine());
        int m = Integer.parseInt(st.nextToken());
        int r = Integer.parseInt(st.nextToken());
        char[] z = br.readLine().trim().toCharArray();
        // TreeSet 维护 '0' 位置及哨兵
        TreeSet<Integer> zeros = new TreeSet<>();
        zeros.add(0);
        zeros.add(m + 1);
        long w = 0;
        for (int i = 1; i <= m; i++) {
            if (z[i - 1] == '0') zeros.add(i);
        }
        int i = 1;
        while (i <= m) {
            if (z[i - 1] == '0') {
                i++;
                continue;
            }
            int j = i;
            while (j <= m && z[j - 1] == '1') j++;
            long len = j - i;
            w += len * (len + 1) / 2;
            i = j;
        }

        StringBuilder out = new StringBuilder();
        for (int t = 0; t < r; t++) {
            int p = Integer.parseInt(br.readLine().trim());
            if (z[p - 1] == '0') {
                int L = zeros.lower(p);
                int R = zeros.higher(p);
                long a = p - L - 1;
                long b = R - p - 1;
                w += (a + 1) * (b + 1);
                zeros.remove(p);
                z[p - 1] = '1';
            } else {
                int L = zeros.lower(p);
                int R = zeros.higher(p);
                long a = p - L - 1;
                long b = R - p - 1;
                w -= (a + 1) * (b + 1);
                zeros.add(p);
                z[p - 1] = '0';
            }
            out.append(w).append('\n');
        }
        System.out.print(out);
    }
}
