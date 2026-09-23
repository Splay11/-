class Solution {
    public int firstTasteLevel(String note) {
        for (int i = 0; i < note.length(); i++) {
            char ch = note.charAt(i);
            if (ch >= '0' && ch <= '9') {
                return ch - '0';
            }
        }
        return -1;
    }
}
