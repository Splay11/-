import java.util.ArrayList;

public class Solution {
    public int countFormableGroups(String a, String b) {
        ArrayList<Character> chars = new ArrayList<>();
        for (int i = 0; i < a.length(); i++) chars.add(a.charAt(i));
        int ans = 0;
        while (true) {
            int j = 0;
            ArrayList<Character> nxt = new ArrayList<>();
            for (char ch : chars) {
                if (j < b.length() && ch == b.charAt(j)) {
                    j++;
                } else {
                    nxt.add(ch);
                }
            }
            if (j == b.length()) {
                ans++;
                chars = nxt;
            } else {
                break;
            }
        }
        return ans;
    }
}
