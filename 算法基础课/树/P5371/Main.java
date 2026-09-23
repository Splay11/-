import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;
import java.util.Queue;
import java.util.Scanner;

public class Main {
    static class TreeNode {
        int val;
        TreeNode left;
        TreeNode right;

        TreeNode(int val) {
            this.val = val;
            this.left = null;
            this.right = null;
        }

        TreeNode(int val, TreeNode left, TreeNode right) {
            this.val = val;
            this.left = left;
            this.right = right;
        }
    }

    static TreeNode build_tree(int[] tree_arr) {
        // 空树：数组为空，或根位置为空（用 -1 表示）
        if (tree_arr == null || tree_arr.length == 0 || tree_arr[0] == -1) {
            return null;
        }

        Queue<TreeNode> q = new LinkedList<TreeNode>();
        TreeNode rt = new TreeNode(tree_arr[0]);
        q.add(rt);

        int index = 1;
        while (!q.isEmpty() && index < tree_arr.length) {
            TreeNode node = q.poll();

            // 左孩子
            if (index < tree_arr.length && tree_arr[index] != -1) {
                node.left = new TreeNode(tree_arr[index]);
                q.add(node.left);
            }
            index++;

            // 右孩子
            if (index < tree_arr.length && tree_arr[index] != -1) {
                node.right = new TreeNode(tree_arr[index]);
                q.add(node.right);
            }
            index++;
        }

        return rt;
    }

    static List<Integer> level_order(TreeNode root) {
        // 层序：只访问非空结点
        List<Integer> res = new ArrayList<Integer>();
        if (root == null) {
            return res;
        }
        Queue<TreeNode> q = new LinkedList<TreeNode>();
        q.add(root);
        while (!q.isEmpty()) {
            TreeNode node = q.poll();
            res.add(node.val);
            if (node.left != null) {
                q.add(node.left);
            }
            if (node.right != null) {
                q.add(node.right);
            }
        }
        return res;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        int[] tree_arr = new int[n];
        for (int i = 0; i < n; i++) {
            tree_arr[i] = sc.nextInt();
        }
        sc.close();

        TreeNode root = build_tree(tree_arr);
        List<Integer> res = level_order(root);
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < res.size(); i++) {
            if (i > 0) {
                sb.append(' ');
            }
            sb.append(res.get(i));
        }
        System.out.println(sb.toString());
    }
}
