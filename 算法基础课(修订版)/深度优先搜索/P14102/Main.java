import java.util.*;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        // 读取数组的长度
        int n = scanner.nextInt();
        int[] nums = new int[n];

        // 读取数组
        for (int i = 0; i < n; i++) {
            nums[i] = scanner.nextInt();
        }

        // 按字典序排序
        Arrays.sort(nums);

        // 初始化数据
        List<List<Integer>> result = new ArrayList<>();
        List<Integer> path = new ArrayList<>();
        boolean[] visited = new boolean[n];

        // 调用 DFS
        dfs(nums, path, visited, result);

        // 输出所有排列
        for (List<Integer> perm : result) {
            // 使用 StringBuilder 拼接结果
            StringBuilder sb = new StringBuilder();
            for (int num : perm) {
                sb.append(num).append(" ");
            }
            System.out.println(sb.toString().trim()); // 去掉末尾多余的空格
        }

        scanner.close();
    }

    public static void dfs(int[] nums, List<Integer> path, boolean[] visited, List<List<Integer>> result) {
        // 终止条件：路径长度等于 nums 长度，说明一个排列生成完毕
        if (path.size() == nums.length) {
            result.add(new ArrayList<>(path)); // 将当前路径加入结果
            return;
        }

        // 遍历每个元素，尝试加入当前路径
        for (int i = 0; i < nums.length; i++) {
            if (!visited[i]) { // 如果当前数字未被访问
                visited[i] = true; // 标记为已访问
                path.add(nums[i]); // 将该数字加入路径
                dfs(nums, path, visited, result); // 递归调用
                path.remove(path.size() - 1); // 回溯，移除路径中的最后一个数字
                visited[i] = false; // 恢复标记为未访问
            }
        }
    }
}
