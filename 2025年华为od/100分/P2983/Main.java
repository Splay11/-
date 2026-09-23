import java.util.ArrayDeque;

public class Solution {
    public int maxBracketDepth(String s) {
        ArrayDeque<Character> stack = new ArrayDeque<>();
        int depth = 0, best = 0;
        for (int i = 0; i < s.length(); i++) {
            char ch = s.charAt(i);
            if (ch == '(' || ch == '[' || ch == '{') {
                stack.push(ch);
                depth++;
                if (depth > best) best = depth;
            } else if (ch == ')' || ch == ']' || ch == '}') {
                char need = ch == ')' ? '(' : (ch == ']' ? '[' : '{');
                if (stack.isEmpty() || stack.pop() != need) return 0;
                depth--;
            } else {
                return 0;
            }
        }
        return stack.isEmpty() ? best : 0;
    }
}
