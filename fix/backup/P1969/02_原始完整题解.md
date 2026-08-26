## 思路：思维
容易想到:反转前缀即可

当k = 0 时，构造arr = 1,2,3,4,...,n

当k = 1 时, 将1,2反转一下:2,1,3,4,...,n

当k = x 时,将1,2,...,x+1这个前缀反转一下:x+1,x,...,1,x+2,...,n


## 代码

### python
```python
n , k = map(int, input().split())
k += 1
arr = [k - i for i in range(k)] + [i + 1 for i in range(k , n)]
print(*arr)
```


OJ会员可以通过点击题目上方《已通过》查看其他通过代码来学习。