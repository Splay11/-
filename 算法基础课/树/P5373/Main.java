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

    static void preorder(TreeNode root, List<Integer> res) {
        // 前序：根 -> 左 -> 右
        if (root == null) {
            return;
        }
        res.add(root.val);
        preorder(root.left, res);
        preorder(root.right, res);
    }

    static void inorder(TreeNode root, List<Integer> res) {
        // 中序：左 -> 根 -> 右
        if (root == null) {
            return;
        }
        inorder(root.left, res);
        res.add(root.val);
        inorder(root.right, res);
    }

    static void postorder(TreeNode root, List<Integer> res) {
        // 后序：左 -> 右 -> 根
        if (root == null) {
            return;
        }
        postorder(root.left, res);
        postorder(root.right, res);
        res.add(root.val);
    }

    static void printLine(List<Integer> res) {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < res.size(); i++) {
            if (i > 0) {
                sb.append(' ');
            }
            sb.append(res.get(i));
        }
        System.out.println(sb.toString());
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

        List<Integer> preRes = new ArrayList<Integer>();
        List<Integer> inRes = new ArrayList<Integer>();
        List<Integer> postRes = new ArrayList<Integer>();
        preorder(root, preRes);
        inorder(root, inRes);
        postorder(root, postRes);

        printLine(preRes);
        printLine(inRes);
        printLine(postRes);
    }
}
