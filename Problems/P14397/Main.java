public class Solution {
    public String processString(String s) {
        StringBuilder digits = new StringBuilder();
        StringBuilder letters = new StringBuilder();
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (c >= '0' && c <= '9') digits.append(c);
            else if (c >= 'A' && c <= 'Z') letters.append(c);
        }
        if (digits.length() == 0 || letters.length() == 0) return s;
        StringBuilder res = new StringBuilder();
        int n = Math.min(digits.length(), letters.length());
        for (int i = 0; i < n; i++) {
            char d = digits.charAt(i);
            res.append(d);
            int cnt = d - '0';
            if (cnt > 0) {
                for (int k = 0; k < cnt; k++) res.append(letters.charAt(i));
            }
        }
        if (digits.length() > n) res.append(digits.substring(n));
        else if (letters.length() > n) res.append(letters.substring(n));
        return res.toString();
    }
}
