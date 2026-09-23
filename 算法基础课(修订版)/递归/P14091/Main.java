import java.util.Scanner;

public class Main{
    // 递归函数：计算最大路径和
    public static int maxPathSum(int[] arr, int index, int n) {
        // 计算当前节点的左子节点和右子节点的索引
        int leftIndex = 2 * index + 1;
        int rightIndex = 2 * index + 2;

        // 如果是叶子节点，直接返回该节点的值
        if (leftIndex >= n && rightIndex >= n) {
            return arr[index];
        }

        int leftSum = 0;
        int rightSum = 0;

        // 如果左子树存在，递归计算左子树的最大路径和
        if (leftIndex < n) {
            leftSum = maxPathSum(arr, leftIndex, n);
        }

        // 如果右子树存在，递归计算右子树的最大路径和
        if (rightIndex < n) {
            rightSum = maxPathSum(arr, rightIndex, n);
        }

        // 返回当前节点的值加上左右子树最大路径和
        return arr[index] + Math.max(leftSum, rightSum);
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        int n = scanner.nextInt(); // 输入节点数
        int[] arr = new int[n];    // 完全二叉树的节点值

        for (int i = 0; i < n; i++) {
            arr[i] = scanner.nextInt();
        }

        // 从根节点开始计算最大路径和
        System.out.println(maxPathSum(arr, 0, n));

        scanner.close();
    }
}
