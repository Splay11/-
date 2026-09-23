import java.io.*;
import java.util.*;

class ListNode {
    long val;
    ListNode next;

    ListNode(long val) {
        this.val = val;
    }
}

public class Main {
    private static List<Long> parseNumbers(String s) {
        List<Long> nums = new ArrayList<>();
        int n = s.length();

        for (int i = 0; i < n; ) {
            char c = s.charAt(i);
            if (c == '-' || Character.isDigit(c)) {
                int sign = 1;
                if (c == '-') {
                    sign = -1;
                    i++;
                }

                long x = 0;
                while (i < n && Character.isDigit(s.charAt(i))) {
                    x = x * 10 + (s.charAt(i) - '0');
                    i++;
                }
                nums.add(x * sign);
            } else {
                i++;
            }
        }

        return nums;
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in, "UTF-8"));
        StringBuilder sb = new StringBuilder();
        String line;

        while ((line = br.readLine()) != null) {
            sb.append(line);
        }

        List<Long> nums = parseNumbers(sb.toString());

        ListNode dummy = new ListNode(0);
        ListNode tail = dummy;
        for (long x : nums) {
            tail.next = new ListNode(x);
            tail = tail.next;
        }

        Solution solution = new Solution();
        System.out.print("\"" + solution.gameResult(dummy.next) + "\"");
    }
}
