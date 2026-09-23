public class Solution {
    public int countOpenSyllables(String s) {
        StringBuilder text = new StringBuilder();
        String[] words = s.split(" ", -1);
        for (int wi = 0; wi < words.length; wi++) {
            if (wi > 0) text.append(' ');
            String w = words[wi];
            boolean pure = w.length() > 0;
            for (int i = 0; i < w.length(); i++) {
                char ch = w.charAt(i);
                if (ch < 'a' || ch > 'z') {
                    pure = false;
                    break;
                }
            }
            if (pure) {
                text.append(new StringBuilder(w).reverse());
            } else {
                text.append(w);
            }
        }

        int ans = 0;
        String t = text.toString();
        for (int i = 0; i + 3 < t.length(); i++) {
            char a = t.charAt(i), b = t.charAt(i + 1), c = t.charAt(i + 2), d = t.charAt(i + 3);
            if (isConsonant(a) && isVowel(b) && isConsonant(c) && c != 'r' && d == 'e') {
                ans++;
            }
        }
        return ans;
    }

    private boolean isVowel(char ch) {
        return ch == 'a' || ch == 'e' || ch == 'i' || ch == 'o' || ch == 'u';
    }

    private boolean isConsonant(char ch) {
        return ch >= 'a' && ch <= 'z' && !isVowel(ch);
    }
}
