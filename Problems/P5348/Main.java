import java.util.Arrays;
import java.util.Scanner;

public class Main {
    static final String WAN = "123456789";
    static final String TONG = "abcdefghi";
    static final String TIAO = "ABCDEFGHI";
    static final String ALL = "123456789abcdefghiABCDEFGHI";

    static int suitOf(char ch) {
        if (WAN.indexOf(ch) >= 0) {
            return 0;
        }
        if (TONG.indexOf(ch) >= 0) {
            return 1;
        }
        return 2;
    }

    static char nextInSuit(char ch, int step) {
        // 同一门里往后数 step 张，跨出门就没有顺子
        String[] groups = {WAN, TONG, TIAO};
        for (int g = 0; g < 3; g++) {
            int pos = groups[g].indexOf(ch);
            if (pos >= 0) {
                int nxt = pos + step;
                if (nxt >= 0 && nxt < 9) {
                    return groups[g].charAt(nxt);
                }
                return 0;
            }
        }
        return 0;
    }

    static int suitCount(int[] cnt) {
        // 统计手里实际出现了几门花色
        int[] used = new int[3];
        for (int i = 0; i < ALL.length(); i++) {
            char ch = ALL.charAt(i);
            if (cnt[ch] > 0) {
                used[suitOf(ch)] = 1;
            }
        }
        return used[0] + used[1] + used[2];
    }

    static boolean tryMelds(int[] cnt) {
        // 把剩下的牌拆成若干顺子或刻子，必须拆空
        char first = 0;
        for (int i = 0; i < ALL.length(); i++) {
            if (cnt[ALL.charAt(i)] > 0) {
                first = ALL.charAt(i);
                break;
            }
        }
        if (first == 0) {
            return true;
        }
        int f = first;
        // 先试刻子：三张相同
        if (cnt[f] >= 3) {
            cnt[f] -= 3;
            if (tryMelds(cnt)) {
                cnt[f] += 3;
                return true;
            }
            cnt[f] += 3;
        }
        // 再试顺子：同一门连续三张
        char a = nextInSuit(first, 1);
        char b = nextInSuit(first, 2);
        if (a != 0 && b != 0 && cnt[a] > 0 && cnt[b] > 0) {
            cnt[f]--;
            cnt[a]--;
            cnt[b]--;
            if (tryMelds(cnt)) {
                cnt[f]++;
                cnt[a]++;
                cnt[b]++;
                return true;
            }
            cnt[f]++;
            cnt[a]++;
            cnt[b]++;
        }
        return false;
    }

    static boolean canHu(int[] cnt) {
        // 14 张、缺一门，并且能拆成 k 组面子加一对将
        int tot = 0;
        for (int i = 0; i < ALL.length(); i++) {
            tot += cnt[ALL.charAt(i)];
        }
        if (tot != 14) {
            return false;
        }
        int sc = suitCount(cnt);
        if (sc < 1 || sc > 2) {
            return false;
        }
        for (int i = 0; i < ALL.length(); i++) {
            int t = ALL.charAt(i);
            if (cnt[t] >= 2) {
                cnt[t] -= 2;
                boolean ok = tryMelds(cnt);
                cnt[t] += 2;
                if (ok) {
                    return true;
                }
            }
        }
        return false;
    }

    static String winningTiles(String hand) {
        // 枚举所有还能再摸的牌面，收集能胡的那些
        int[] cnt = new int[128];
        for (int i = 0; i < hand.length(); i++) {
            cnt[hand.charAt(i)]++;
        }
        StringBuilder ans = new StringBuilder();
        for (int i = 0; i < ALL.length(); i++) {
            int t = ALL.charAt(i);
            if (cnt[t] >= 4) {
                continue;
            }
            cnt[t]++;
            if (canHu(cnt)) {
                ans.append(ALL.charAt(i));
            }
            cnt[t]--;
        }
        if (ans.length() == 0) {
            return "-1";
        }
        // 题面要求按 ASCII 从小到大输出
        char[] cs = ans.toString().toCharArray();
        Arrays.sort(cs);
        return new String(cs);
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String s = sc.next();
        System.out.println(winningTiles(s));
        sc.close();
    }
}
