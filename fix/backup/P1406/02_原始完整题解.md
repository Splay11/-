用栈模拟这个过程即可。具体细节见代码
~~~java
import java.util.*;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        String s = scanner.nextLine();
        Stack<String> stack = new Stack<>();
        for (char x : s.toCharArray()) {
            // 忽略空格
            if (x == ' ') {
                continue;
            }
            // 左括号实际也没用
            if (x == '(') {
                continue;
            }
            // 每次遇到右括号，栈的顶部一定形如: ... op val1 , val2 , ... valk 
            // 那么计算就是 valk op valk-1 op ... op val1
            /*
                举个实际的例子，比如遇到右括号时，
                
                栈是: (前面一段blabla是什么不用管) - 1 3 2
                那么就是进行: 2 - 3 - 1 , 得到 -2 , 然后再放入栈中
                
                栈是: (前面一段blabla是什么不用管) * 2 3
                那么就是进行: 3 * 2 , 得到 6，再放入栈中
            */
            if (x == ')') {
                String op = "";
                List<Integer> val = new ArrayList<>();
                while (!stack.empty() && !isOperator(stack.peek())) {
                    val.add(Integer.parseInt(stack.pop()));
                }
                op = stack.pop();
                Collections.reverse(val);
                stack.push(String.valueOf(calc(op, val)));
            } else {
                stack.push(String.valueOf(x));
            }
        }
        System.out.println(stack.pop());
    }
    public static int calc(String op, List<Integer> val) {
        int res = val.get(0);
        for (int i = 1; i < val.size(); i++) {
            if (op.equals("+")) {
                res += val.get(i);
            } else if (op.equals("-")) {
                res -= val.get(i);
            } else {
                res *= val.get(i);
            }
        }
        return res;
    }

    public static boolean isOperator(String op) {
        return op.equals("+") || op.equals("-") || op.equals("*");
    }
}
~~~