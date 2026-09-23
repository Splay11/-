public class Solution {
    public String rearrangeSN(String sn, int m) {
        // 异常字符：非字母数字且非破折号
        for (int i = 0; i < sn.length(); i++) {
            char c = sn.charAt(i);
            if (!Character.isLetterOrDigit(c) && c != '-') return "";
        }

        StringBuilder chars = new StringBuilder();
        for (int i = 0; i < sn.length(); i++) {
            char c = sn.charAt(i);
            if (Character.isLetterOrDigit(c)) {
                chars.append(Character.toUpperCase(c));
            }
        }
        if (chars.length() == 0) return "";

        int n = chars.length();
        int rem = n % m;
        StringBuilder ans = new StringBuilder();
        int idx = 0;
        // 首段承接余数长度
        if (rem != 0) {
            if (ans.length() > 0) ans.append('-');
            ans.append(chars, idx, idx + rem);
            idx += rem;
        }
        while (idx < n) {
            if (ans.length() > 0) ans.append('-');
            ans.append(chars, idx, idx + m);
            idx += m;
        }
        return ans.toString();
    }
}
