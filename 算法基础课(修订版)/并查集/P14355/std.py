# 输入联系人数量
num = int(input())

# 输入联系人姓名及其电话号码，并按行存储
arr = [input().split() for _ in range(num)]

# 创建一个字典，用于映射电话号码到对应的联系人编号列表
phone_to_id = {}

# 遍历每个联系人，将他们的电话号码加入映射字典中
for i in range(num):
    for phone in arr[i][1:]:
        if phone in phone_to_id:
            # 如果电话号码已经存在，添加当前联系人编号到列表中
            phone_to_id[phone].append(i)
        else:
            # 如果电话号码不存在，初始化一个列表并存储联系人编号
            phone_to_id[phone] = [i]

# 初始化并查集，每个联系人最初是自己所在组的代表
fa = [i for i in range(num)]

# 查找函数（带路径压缩），查找当前联系人所在组的根节点
def find(x):
    if x != fa[x]:
        fa[x] = find(fa[x])  # 路径压缩
    return fa[x]

# 合并两个组，将两个联系人的组合并到一起
def merge(x, y):
    x = find(x)
    y = find(y)
    if x != y:
        fa[x] = y  # 合并操作

# 判断两个联系人是否属于同一组
def same(x, y):
    return find(x) == find(y)

# 遍历每个电话号码，将共享同一电话号码的联系人合并到同一组
for phone in phone_to_id:
    first_id = phone_to_id[phone][0]  # 获取第一个联系人的编号
    for i in range(1, len(phone_to_id[phone])):
        merge(first_id, phone_to_id[phone][i])  # 合并其他拥有相同电话号码的联系人

# 创建字典，用于存储每个组的最小字典序的姓名和所有电话号码
root_to_name = {}
root_to_phones = {}

# 遍历每个联系人，按组进行合并处理
for i in range(num):
    root = find(i)  # 查找联系人的根节点（代表组）

    # 如果该组已经有一个名字，则比较字典序
    if root in root_to_name:
        # 更新为字典序更小的姓名
        if arr[i][0] <= root_to_name[root]:
            root_to_name[root] = arr[i][0]
    else:
        # 如果该组还没有姓名，则赋值当前联系人的姓名
        root_to_name[root] = arr[i][0]

    # 合并该联系人的所有电话号码到所在组
    for phone in arr[i][1:]:
        if root in root_to_phones:
            # 如果该组已经有电话号码，则继续添加
            root_to_phones[root].add(phone)
        else:
            # 如果该组没有电话号码，则初始化一个集合并添加
            root_to_phones[root] = {phone}

# 结果存储列表
res = []

# 构建结果列表，包含每个组的姓名及电话号码（按字典序排序）
for root in root_to_name:
    res.append([root_to_name[root]] + sorted(list(root_to_phones[root])))

# 对结果列表进行排序
res.sort()

# 输出合并后的联系人姓名及电话号码
for x in res:
    print(' '.join(x))
