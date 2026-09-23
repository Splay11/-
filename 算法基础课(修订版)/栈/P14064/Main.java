import java.util.*;

public class Main {
   // 定义栈的最大容量
   static final int MAXN = 1010;

   public static void main(String[] args) {
       Scanner sc = new Scanner(System.in);
       // 用数组模拟栈
       long[] stack = new long[MAXN];
       // 栈顶指针
       int top = 0;
       
       // 读取输入数组并转换为整数列表
       List<Long> arr = new ArrayList<>();
       String[] inputs = sc.nextLine().split(" ");
       for (String s : inputs) {
           arr.add(Long.parseLong(s));
       }
       
       // 处理每个输入的数字x
       for (long x : arr) {
           // 循环检查是否需要合并栈内元素
           while (true) {
               boolean flag = false; // 标记是否发生合并
               long tmp = 0L; // 存储连续元素之和
               
               // 从栈顶往下遍历，计算连续元素之和
               for (int i = top; i >= 0; i--) {
                   tmp += stack[i];
                   
                   // 如果和等于当前数字x，执行合并操作
                   if (tmp == x) {
                       x += tmp; // 新数字为原数字的2倍
                       top = i - 1; // 更新栈顶指针
                       flag = true; // 标记已合并
                       break;
                   }
               }
               
               // 如果没有可以合并的元素，退出循环
               if (!flag) break;
           }
           
           // 将处理后的数字压入栈顶
           stack[++top] = x;
       }
       
       // 从栈顶开始输出所有元素
       while (top > 0) {
           System.out.print(stack[top] + " ");
           top--;
       }
       System.out.println();
       sc.close();
   }
}
