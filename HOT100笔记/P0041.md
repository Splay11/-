前置知识：

1.[二叉树基础知识](https://codefun2000.com/codenote/hot100/P0039)

2.[面试手撕中二叉树的读入与构建](https://codefun2000.com/codenote/hot100/P0040#)

3.[轻松掌握广度优先搜索(BFS)算法](https://codefun2000.com/codenote/hot100/P0035)  - 搞懂基础BFS算法 外加 岛屿数量！

## LeetCode 102. 二叉树的层序遍历

[在线刷题](https://codefun2000.com/p/P4057)

给你二叉树的根节点$root$ ，输出其节点值的层序遍历。 （即逐层地，从左到右访问所有节点）。

**输入描述**

一行包含二叉树的序列化数组，节点值之间用空格隔开，空节点用null表示。

**输出描述**


从$root_0$开始层序遍历，每层一行输出，一行里的数字之间以空格分隔。（不输出空节点）


## 样例1 

![img](https://assets.leetcode.com/uploads/2021/02/19/tree1.jpg)

**输入** 

```
3 9 20 null null 15 7
```

**输出** 

```
3
9 20
15 7
```

**思路**

根据**前置知识** ， 我们只需要先构建出二叉树。然后对二叉树进行层序遍历即可。

**方法一：改造的BFS算法流程**

由于本题需要我们每一行打印同一层的节点，我们可以**改造一下朴素的BFS算法流程：每次把队列里所有节点都拿出来，然后拓展节点，而不是像朴素的BFS那样每次只拿一个节点出来拓展新的节点。**

**用一个动画大家就知道是怎么回事了👇**

@[video](https://codefun2000.com/p/4117/file/%E5%B1%82%E5%BA%8F%E9%81%8D%E5%8E%861.mp4)

**将上述动画形式化一下👇**

![](/file/2/-9k1Fv6rUkDF-cBiUdglG.png)



不难发现，这种BFS算法，也可以理解为是：两个数组来回迭代。每次通过`q`数组拓展左右儿子节点得到`q_next_level` 数组。然后再把`q_next_level` 赋值回`q`。

**代码实现👇**
#code-switcher
```python id="9mekd8"
class Solution:
    def levelOrder(self, root):
        # 空树直接返回空数组
        if not root:
            return []

        # q 存放当前层的所有节点
        q = [root]

        # res 存放最终答案
        res = []

        # 每一轮处理一整层节点
        while q:
            # val_arr 记录当前层的节点值
            val_arr = []

            # q_next_level 存放下一层的所有节点
            q_next_level = []

            # 从左到右遍历当前层所有节点
            for node in q:
                val_arr.append(node.val)

                # 拓展左孩子
                if node.left:
                    q_next_level.append(node.left)

                # 拓展右孩子
                if node.right:
                    q_next_level.append(node.right)

            # 当前层结果加入答案
            res.append(val_arr)

            # 进入下一层
            q = q_next_level

        return res
```

```cpp id="5adkc7"
class Solution {
public:
    vector<vector<int>> levelOrder(TreeNode* root) {
        // 空树直接返回空数组
        if (root == nullptr) {
            return vector<vector<int>>();
        }

        // q 存放当前层的所有节点
        vector<TreeNode*> q;
        q.push_back(root);

        // res 存放最终答案
        vector<vector<int>> res;

        // 每一轮处理一整层节点
        while (!q.empty()) {
            // val_arr 记录当前层的节点值
            vector<int> val_arr;

            // q_next_level 存放下一层的所有节点
            vector<TreeNode*> q_next_level;

            // 从左到右遍历当前层所有节点
            for (TreeNode* node : q) {
                val_arr.push_back(node->val);

                // 拓展左孩子
                if (node->left != nullptr) {
                    q_next_level.push_back(node->left);
                }

                // 拓展右孩子
                if (node->right != nullptr) {
                    q_next_level.push_back(node->right);
                }
            }

            // 当前层结果加入答案
            res.push_back(val_arr);

            // 进入下一层
            q = q_next_level;
        }

        return res;
    }
};
```

```java id="528dzo"
class Solution {
    public List<List<Integer>> levelOrder(TreeNode root) {
        // res 存放最终答案
        List<List<Integer>> res = new ArrayList<List<Integer>>();

        // 空树直接返回空数组
        if (root == null) {
            return res;
        }

        // q 存放当前层的所有节点
        List<TreeNode> q = new ArrayList<TreeNode>();
        q.add(root);

        // 每一轮处理一整层节点
        while (!q.isEmpty()) {
            // valArr 记录当前层的节点值
            List<Integer> valArr = new ArrayList<Integer>();

            // qNextLevel 存放下一层的所有节点
            List<TreeNode> qNextLevel = new ArrayList<TreeNode>();

            // 从左到右遍历当前层所有节点
            for (TreeNode node : q) {
                valArr.add(node.val);

                // 拓展左孩子
                if (node.left != null) {
                    qNextLevel.add(node.left);
                }

                // 拓展右孩子
                if (node.right != null) {
                    qNextLevel.add(node.right);
                }
            }

            // 当前层结果加入答案
            res.add(valArr);

            // 进入下一层
            q = qNextLevel;
        }

        return res;
    }
}
```

```go id="t4t7z7"
func levelOrder(root *TreeNode) [][]int {
	// 空树直接返回空数组
	if root == nil {
		return [][]int{}
	}

	// q 存放当前层的所有节点
	q := []*TreeNode{root}

	// res 存放最终答案
	res := make([][]int, 0)

	// 每一轮处理一整层节点
	for len(q) > 0 {
		// valArr 记录当前层的节点值
		valArr := make([]int, 0)

		// qNextLevel 存放下一层的所有节点
		qNextLevel := make([]*TreeNode, 0)

		// 从左到右遍历当前层所有节点
		for _, node := range q {
			valArr = append(valArr, node.Val)

			// 拓展左孩子
			if node.Left != nil {
				qNextLevel = append(qNextLevel, node.Left)
			}

			// 拓展右孩子
			if node.Right != nil {
				qNextLevel = append(qNextLevel, node.Right)
			}
		}

		// 当前层结果加入答案
		res = append(res, valArr)

		// 进入下一层
		q = qNextLevel
	}

	return res
}
```

```javascript id="b99l9f"
var levelOrder = function(root) {
    // 空树直接返回空数组
    if (root === null) {
        return [];
    }

    // q 存放当前层的所有节点
    let q = [root];

    // res 存放最终答案
    let res = [];

    // 每一轮处理一整层节点
    while (q.length > 0) {
        // valArr 记录当前层的节点值
        let valArr = [];

        // qNextLevel 存放下一层的所有节点
        let qNextLevel = [];

        // 从左到右遍历当前层所有节点
        for (let node of q) {
            valArr.push(node.val);

            // 拓展左孩子
            if (node.left !== null) {
                qNextLevel.push(node.left);
            }

            // 拓展右孩子
            if (node.right !== null) {
                qNextLevel.push(node.right);
            }
        }

        // 当前层结果加入答案
        res.push(valArr);

        // 进入下一层
        q = qNextLevel;
    }

    return res;
};
```

```c id="t87dqw"
int** levelOrder(struct TreeNode* root, int* returnSize, int** returnColumnSizes) {
    // 空树直接返回空数组
    if (root == NULL) {
        *returnSize = 0;
        *returnColumnSizes = (int*)malloc(sizeof(int) * 0);
        return (int**)malloc(sizeof(int*) * 0);
    }

    // res 存放最终答案
    int** res = (int**)malloc(sizeof(int*) * 100005);
    *returnColumnSizes = (int*)malloc(sizeof(int) * 100005);
    *returnSize = 0;

    // q 存放当前层的所有节点
    struct TreeNode** q = (struct TreeNode**)malloc(sizeof(struct TreeNode*) * 100005);
    int qSize = 0;
    q[qSize++] = root;

    // 每一轮处理一整层节点
    while (qSize > 0) {
        // valArr 记录当前层的节点值
        int* valArr = (int*)malloc(sizeof(int) * qSize);

        // qNextLevel 存放下一层的所有节点
        struct TreeNode** qNextLevel = (struct TreeNode**)malloc(sizeof(struct TreeNode*) * 100005);
        int nextSize = 0;

        // 从左到右遍历当前层所有节点
        for (int i = 0; i < qSize; i++) {
            struct TreeNode* node = q[i];
            valArr[i] = node->val;

            // 拓展左孩子
            if (node->left != NULL) {
                qNextLevel[nextSize++] = node->left;
            }

            // 拓展右孩子
            if (node->right != NULL) {
                qNextLevel[nextSize++] = node->right;
            }
        }

        // 当前层结果加入答案
        res[*returnSize] = valArr;
        (*returnColumnSizes)[*returnSize] = qSize;
        (*returnSize)++;

        // 进入下一层
        free(q);
        q = qNextLevel;
        qSize = nextSize;
    }

    free(q);
    return res;
}
```

#code-switcher
**方法二：BFS + 记录层数**

有没有什么方法，**不去改造BFS本身的算法结构**，直接在BFS过程中得到结果呢？

我们可以记录当前BFS从根到这个节点的步数。这个步数就是树的层数。由于在算法一开始我们并不知道这个树有多少层，所以需要维护一个可变长的二维数组。每次从队头访问到一个新的节点时，将这个节点按层数插入到这个结果数组。

假设节点$i$的层数是$dep_i$ , 那么分两种情况：

1.如果$length(res) < dep_i$ ， 那么需要新开辟一行数组：在$res$的末尾加一个数组`[i]`  

2.如果$length(res) >= dep_i$ , 那么只需要将结果插入到对应的那一行即可：`res[dep[i]].append(i)`

**用一个动画为大家演示一下👇**

@[video](https://codefun2000.com/p/4117/file/%E5%B1%82%E5%BA%8F%E9%81%8D%E5%8E%862.mp4)

**代码实现👇**
#code-switcher
```python id="yd2cn5"
class Solution:
    def levelOrder(self, root):
        # 空树直接返回空数组
        if not root:
            return []

        # 队列中同时记录节点和它所在的层数
        q = [(root, 0)]

        # res[i] 表示第 i 层的所有节点值
        res = []

        # 普通 BFS，每次从队头取出一个节点
        while q:
            node, dep = q.pop(0)

            # 如果当前层还没有创建，就新建一层
            if len(res) <= dep:
                res.append([node.val])
            else:
                # 否则直接加入对应层
                res[dep].append(node.val)

            # 先加入左儿子，再加入右儿子，保证从左到右
            if node.left:
                q.append((node.left, dep + 1))

            if node.right:
                q.append((node.right, dep + 1))

        return res
```

```cpp id="cfi482"
class Solution {
public:
    vector<vector<int>> levelOrder(TreeNode* root) {
        // 空树直接返回空数组
        if (root == nullptr) {
            return vector<vector<int>>();
        }

        // 队列中同时记录节点和它所在的层数
        vector<pair<TreeNode*, int>> q;
        q.push_back({root, 0});

        // res[i] 表示第 i 层的所有节点值
        vector<vector<int>> res;

        // 普通 BFS，每次从队头取出一个节点
        while (!q.empty()) {
            TreeNode* node = q[0].first;
            int dep = q[0].second;
            q.erase(q.begin());

            // 如果当前层还没有创建，就新建一层
            if ((int)res.size() <= dep) {
                res.push_back(vector<int>{node->val});
            } else {
                // 否则直接加入对应层
                res[dep].push_back(node->val);
            }

            // 先加入左儿子，再加入右儿子，保证从左到右
            if (node->left != nullptr) {
                q.push_back({node->left, dep + 1});
            }

            if (node->right != nullptr) {
                q.push_back({node->right, dep + 1});
            }
        }

        return res;
    }
};
```

```java id="0wk9ri"
class Solution {
    public List<List<Integer>> levelOrder(TreeNode root) {
        // res[i] 表示第 i 层的所有节点值
        List<List<Integer>> res = new ArrayList<List<Integer>>();

        // 空树直接返回空数组
        if (root == null) {
            return res;
        }

        // qNode 记录节点，qDep 记录对应节点所在层数
        List<TreeNode> qNode = new ArrayList<TreeNode>();
        List<Integer> qDep = new ArrayList<Integer>();

        qNode.add(root);
        qDep.add(0);

        // 普通 BFS，每次从队头取出一个节点
        while (!qNode.isEmpty()) {
            TreeNode node = qNode.remove(0);
            int dep = qDep.remove(0);

            // 如果当前层还没有创建，就新建一层
            if (res.size() <= dep) {
                List<Integer> level = new ArrayList<Integer>();
                level.add(node.val);
                res.add(level);
            } else {
                // 否则直接加入对应层
                res.get(dep).add(node.val);
            }

            // 先加入左儿子，再加入右儿子，保证从左到右
            if (node.left != null) {
                qNode.add(node.left);
                qDep.add(dep + 1);
            }

            if (node.right != null) {
                qNode.add(node.right);
                qDep.add(dep + 1);
            }
        }

        return res;
    }
}
```

```go id="8dfmye"
func levelOrder(root *TreeNode) [][]int {
	// 空树直接返回空数组
	if root == nil {
		return [][]int{}
	}

	// qNode 记录节点，qDep 记录对应节点所在层数
	qNode := []*TreeNode{root}
	qDep := []int{0}

	// res[i] 表示第 i 层的所有节点值
	res := make([][]int, 0)

	// 普通 BFS，每次从队头取出一个节点
	for len(qNode) > 0 {
		node := qNode[0]
		dep := qDep[0]

		qNode = qNode[1:]
		qDep = qDep[1:]

		// 如果当前层还没有创建，就新建一层
		if len(res) <= dep {
			res = append(res, []int{node.Val})
		} else {
			// 否则直接加入对应层
			res[dep] = append(res[dep], node.Val)
		}

		// 先加入左儿子，再加入右儿子，保证从左到右
		if node.Left != nil {
			qNode = append(qNode, node.Left)
			qDep = append(qDep, dep+1)
		}

		if node.Right != nil {
			qNode = append(qNode, node.Right)
			qDep = append(qDep, dep+1)
		}
	}

	return res
}
```

```javascript id="s1ovrv"
var levelOrder = function(root) {
    // 空树直接返回空数组
    if (root === null) {
        return [];
    }

    // 队列中同时记录节点和它所在的层数
    let q = [[root, 0]];
    let head = 0;

    // res[i] 表示第 i 层的所有节点值
    let res = [];

    // 普通 BFS，每次从队头取出一个节点
    while (head < q.length) {
        let cur = q[head];
        head++;

        let node = cur[0];
        let dep = cur[1];

        // 如果当前层还没有创建，就新建一层
        if (res.length <= dep) {
            res.push([node.val]);
        } else {
            // 否则直接加入对应层
            res[dep].push(node.val);
        }

        // 先加入左儿子，再加入右儿子，保证从左到右
        if (node.left !== null) {
            q.push([node.left, dep + 1]);
        }

        if (node.right !== null) {
            q.push([node.right, dep + 1]);
        }
    }

    return res;
};
```

```c 
int** levelOrder(struct TreeNode* root, int* returnSize, int** returnColumnSizes) {
    // 空树直接返回空数组
    if (root == NULL) {
        *returnSize = 0;
        *returnColumnSizes = (int*)malloc(sizeof(int) * 0);
        return (int**)malloc(sizeof(int*) * 0);
    }

    // res[i] 表示第 i 层的所有节点值
    int** res = (int**)malloc(sizeof(int*) * 100005);
    *returnColumnSizes = (int*)malloc(sizeof(int) * 100005);
    *returnSize = 0;

    // qNode 记录节点，qDep 记录对应节点所在层数
    struct TreeNode** qNode = (struct TreeNode**)malloc(sizeof(struct TreeNode*) * 100005);
    int* qDep = (int*)malloc(sizeof(int) * 100005);

    int head = 0;
    int tail = 0;

    qNode[tail] = root;
    qDep[tail] = 0;
    tail++;

    // 普通 BFS，每次从队头取出一个节点
    while (head < tail) {
        struct TreeNode* node = qNode[head];
        int dep = qDep[head];
        head++;

        // 如果当前层还没有创建，就新建一层
        if (*returnSize <= dep) {
            res[*returnSize] = (int*)malloc(sizeof(int) * 100005);
            (*returnColumnSizes)[*returnSize] = 0;
            (*returnSize)++;
        }

        // 将当前节点值加入对应层
        res[dep][(*returnColumnSizes)[dep]] = node->val;
        (*returnColumnSizes)[dep]++;

        // 先加入左儿子，再加入右儿子，保证从左到右
        if (node->left != NULL) {
            qNode[tail] = node->left;
            qDep[tail] = dep + 1;
            tail++;
        }

        if (node->right != NULL) {
            qNode[tail] = node->right;
            qDep[tail] = dep + 1;
            tail++;
        }
    }

    free(qNode);
    free(qDep);

    return res;
}
```

#code-switcher
**面试问答**

**本题的思路是什么？(方法1)**
类似BFS的思路：开始先把根节点放入队列，然后BFS的过程中每次把队列里所有节点一次性拿出来，记录答案。然后从左到右依次拓展它们的左右儿子节点，得到下一层的所有节点，放入队列。如此往复，直到队列为空。

时间复杂度:$O(n)$ , 因为每个节点只会被访问一次。

空间复杂度:$O(n)$ , 开销来自于队列