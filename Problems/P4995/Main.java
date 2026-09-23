import java.io.*;
import java.util.*;

public class Main {
    static String applyOnce(String s) {
        int n = s.length();
        char[] arr = s.toCharArray();
        int[] freq = new int[26];
        int[] left = new int[26];
        for (char ch : arr) freq[ch - 'a']++;
        for (int i = 0; i < n; i++) {
            int c = arr[i] - 'a';
            int x = left[c];
            int y = freq[c] - left[c] - 1;
            if (x == y) {
                freq[c]--;
                int nc = (c + 1) % 26;
                arr[i] = (char) ('a' + nc);
                freq[nc]++;
                left[nc]++;
            } else {
                left[c]++;
            }
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
                if (nxt.equals(z)) break;
                z = nxt;
                window.addLast(z);
                if (window.size() > 27) window.removeFirst();
                if (window.size() == 27) {
                    String first = window.peekFirst();
                    String last = window.peekLast();
                    if (first.equals(last)) {
                        int rem = r - done;
                        String s0 = first;
                        Iterator<String> it = window.iterator();
                        it.next();
                        String s1 = it.next();
                        int add = rem % 26;
                        char[] arr = z.toCharArray();
                        for (int i = 0; i < m; i++) {
                            if (s0.charAt(i) != s1.charAt(i)) {
                                int c = (arr[i] - 'a' + add) % 26;
                                arr[i] = (char) ('a' + c);
                            }
                        }
                        z = new String(arr);
                        break;
                    }
                }
            }
            out.append(z).append('\n');
        }
        System.out.print(out);
    }
}
