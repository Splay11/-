import java.io.*;
import java.util.*;

public class Main {
    // 对串做一次从左到右的平衡字母变换
    static String applyOnce(String s) {
        int n = s.length();
        char[] arr = s.toCharArray();
        int[] freq = new int[26], left = new int[26];
        for (char ch : arr) freq[ch - 'a']++;
        for (int i = 0; i < n; i++) {
            int c = arr[i] - 'a';
            if (left[c] == freq[c] - left[c] - 1) {
                freq[c]--;
                int nc = (c + 1) % 26;
                arr[i] = (char) ('a' + nc);
                freq[nc]++;
                left[nc]++;
            } else left[c]++;
        }
        return new String(arr);
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int q = Integer.parseInt(br.readLine().trim());
        StringBuilder out = new StringBuilder();
        while (q-- > 0) {
            StringTokenizer st = new StringTokenizer(br.readLine());
            int m = Integer.parseInt(st.nextToken());
            int r = Integer.parseInt(st.nextToken());
            String z = br.readLine().trim();
            ArrayDeque<String> window = new ArrayDeque<>();
            window.addLast(z);
            int done = 0;
            while (done < r) {
                String nxt = applyOnce(z);
                done++;
                if (nxt.equals(z)) break; // 已稳定
                z = nxt;
                window.addLast(z);
                if (window.size() > 27) window.removeFirst();
                if (window.size() == 27 && window.peekFirst().equals(window.peekLast())) {
                    // 周期 26：对会变位置加上剩余步数
                    int rem = r - done;
                    String s0 = window.peekFirst();
                    Iterator<String> it = window.iterator();
                    it.next();
                    String s1 = it.next();
                    int add = rem % 26;
                    char[] arr = z.toCharArray();
                    for (int i = 0; i < m; i++) {
                        if (s0.charAt(i) != s1.charAt(i)) {
                            arr[i] = (char) ('a' + (arr[i] - 'a' + add) % 26);
                        }
                    }
                    z = new String(arr);
                    break;
                }
            }
            out.append(z).append('\n');
        }
        System.out.print(out);
    }
}
