class Solution {
    public String reviseMarks(String s) {
        int i0 = -1, i1 = -1;
        int n = s.length();
        for (int i = 0; i < n; i++) {
            char ch = s.charAt(i);
            if (ch == '0' && i0 < 0) i0 = i;
            if (ch == '1' && i1 < 0) i1 = i;
            if (i0 >= 0 && i1 >= 0) break;
        }
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < n; i++) {
            if (i != i0 && i != i1) sb.append(s.charAt(i));
        }
        return sb.toString();
    }
}
