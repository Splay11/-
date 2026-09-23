# 读入
R = list(map(int,input().split()))
cnt = int(input())
# 查询数组里的第i位值
def check (i):
    su = 0
    for x in R:
        su += min(i , x)
    return su <= cnt
# 设定v的边界
l , r = 0 , 10**9
while l <= r:
    mid = l + r >> 1
    if check(mid):
        l = mid + 1
    else:
        r = mid - 1
# 这种情况即题目描述的第一种情况,等价于"数组"全1 , 那么右端点不会动
if r == 10**9:
    r = -1
print(r)
