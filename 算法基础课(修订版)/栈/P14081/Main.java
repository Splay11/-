import java.util.*;

public class Main {
    public static void main(String[] args) {
        // 输入数组：可以从控制台读取或直接定义
        var scanner = new Scanner(System.in);
        var list = new ArrayList<Integer>();
        while (scanner.hasNextInt()) {
            list.add(scanner.nextInt());
        }
        scanner.close();

        // 定义一个栈来存储元素
        var stack = new Stack<Integer>();

        // 遍历数组，模拟消消乐过程
        for (var num : list) {
            stack.push(num); // 将当前元素压入栈

            // 检查栈顶的三个元素是否相同
            if (stack.size() >= 3) {
                var top1 = stack.pop();
                var top2 = stack.pop();
                var top3 = stack.pop();

                if (top1 == top2 && top2 == top3) {
                    // 如果三个元素相同，则消除（不放回栈）
                    continue;
                } else {
                    // 如果不相同，将弹出的元素按原顺序放回栈
                    stack.push(top3);
                    stack.push(top2);
                    stack.push(top1);
                }
            }
        }

        // 将栈中的元素存入结果列表（栈是逆序的）
        var result = new ArrayList<Integer>();
        while (!stack.isEmpty()) {
            result.add(stack.pop());
        }

        // 逆序结果以恢复原始顺序
        Collections.reverse(result);

        // 输出最终结果
        if (result.isEmpty()) {
            System.out.println("[]");
        } else {
            var output = new StringBuilder();
            for (var i = 0; i < result.size(); i++) {
                if (i > 0) output.append(" ");
                output.append(result.get(i));
            }
            System.out.println(output);
        }
    }
}
