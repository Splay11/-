public class Solution {
    public int minDistinctAfterSwap(String resA, String resB) {
        int[] countA = new int[26];
        int[] countB = new int[26];
        for (int i = 0; i < resA.length(); i++) {
            countA[resA.charAt(i) - 'a']++;
        }
        for (int i = 0; i < resB.length(); i++) {
            countB[resB.charAt(i) - 'a']++;
        }

        int dA = 0, dB = 0;
        for (int i = 0; i < 26; i++) {
            if (countA[i] > 0) dA++;
            if (countB[i] > 0) dB++;
        }

        int ans = -1;
        for (int a = 0; a < 26; a++) {
            if (countA[a] == 0) continue;
            for (int b = 0; b < 26; b++) {
                if (countB[b] == 0) continue;
                int cand;
                if (a == b) {
                    if (dA != dB) continue;
                    cand = dA;
                } else {
                    int da = dA - (countA[a] == 1 ? 1 : 0) + (countA[b] == 0 ? 1 : 0);
                    int db = dB - (countB[b] == 1 ? 1 : 0) + (countB[a] == 0 ? 1 : 0);
                    if (da != db) continue;
                    cand = da;
                }
                if (ans == -1 || cand < ans) ans = cand;
            }
        }
        return ans;
    }
}
