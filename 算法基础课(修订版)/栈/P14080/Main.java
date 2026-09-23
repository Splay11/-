import java.util.Stack;

public class Main {
    public static void main(String[] args) {
        // 输入括号字符串
        java.util.Scanner scanner = new java.util.Scanner(System.in);
        String s = scanner.next();  
        Stack<Character> stack = new Stack<>();  // 创建一个栈

        // 遍历字符串中的每个字符
        for (char ch : s.toCharArray()) {
            if (ch == '(') {
                stack.push(ch);  // 遇到左括号，压入栈中
            } else {
                // 遇到右括号时，检查栈是否为空
                if (stack.empty()) {
                    System.out.println("No");  // 栈为空，说明没有匹配的左括号
                    return;
                }
                stack.pop();  // 弹出栈顶元素，匹配对应的左括号
            }
        }

        // 如果栈为空，说明所有左括号都有匹配
        System.out.println(stack.empty() ? "Yes" : "No");  // 输出结果
    }
}
