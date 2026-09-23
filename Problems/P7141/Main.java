import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.util.Arrays;

public class Main {
    // 对每个字母记下第一次和最后一次出现的下标
    // 若某字母至少出现两次，中间长度为 last-first-1（不含两端）
    static int solve(String s) {
        int[] first = new int[26];
        int[] last = new int[26];
        Arrays.fill(first, -1);
        Arrays.fill(last, -1);
        for (int i = 0; i < s.length(); i++) {
            int id = s.charAt(i) - 'a';
            if (first[id] == -1) {
                first[id] = i;
            }
            last[id] = i;
        }
        int ans = -1;
        for (int c = 0; c < 26; c++) {
            if (first[c] != -1 && last[c] > first[c]) {
                // 只统计出现至少两次的字母
                int length = last[c] - first[c] - 1;
                if (length > ans) {
                    ans = length;
                }
            }
        }
        return ans;
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String s = br.readLine();
        System.out.println(solve(s));
    }
}
