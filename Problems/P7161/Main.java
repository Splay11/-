import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.util.ArrayList;

public class Main {
    // 每个字母取在所有串中出现次数的最小值，再按字典序展开
    static ArrayList<Character> solve(String[] words) {
        int[] minCnt = new int[26];
        for (int i = 0; i < 26; i++) {
            minCnt[i] = 1000000000;
        }
        for (int t = 0; t < words.length; t++) {
            int[] cnt = new int[26];
            String w = words[t];
            for (int i = 0; i < w.length(); i++) {
                cnt[w.charAt(i) - 'a']++;
            }
            for (int i = 0; i < 26; i++) {
                if (cnt[i] < minCnt[i]) {
                    minCnt[i] = cnt[i];
                }
            }
        }
        ArrayList<Character> chars = new ArrayList<Character>();
        for (int i = 0; i < 26; i++) {
            // 按 a..z 顺序重复输出 min 次
            for (int k = 0; k < minCnt[i]; k++) {
                chars.add((char) ('a' + i));
            }
        }
        return chars;
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        String[] words = new String[n];
        for (int i = 0; i < n; i++) {
            words[i] = br.readLine().trim();
        }
        ArrayList<Character> chars = solve(words);
        System.out.println(chars.size());
        // 没有公共字符时只输出 0，不再打第二行
        if (!chars.isEmpty()) {
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < chars.size(); i++) {
                if (i > 0) {
                    sb.append(' ');
                }
                sb.append(chars.get(i));
            }
            System.out.println(sb.toString());
        }
    }
}
