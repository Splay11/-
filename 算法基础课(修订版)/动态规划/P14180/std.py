N=int(input())
box=[]
for _ in range(N):
    box.append(list(map(int,input().split())))

box.sort(key=lambda x:(x[0],x[1],x[2])) #升序排序

dp=[0]*N #对于每个盒子作为最底层，其可以获得的最大高度是多少

for i in range(N):
    dp[i]=box[i][2] #是其自己的高度
    for j in range(i):
        #遍历前面的盒子
        #如果比前一个盒子的长宽高都大，那就是自己的高度再加上j盒子的最大高度
        if box[i][0]>box[j][0] and box[i][1]>box[j][1] and box[i][2]>box[j][2]:
            dp[i]=max(dp[i],dp[j]+box[i][2])

print(max(dp))
