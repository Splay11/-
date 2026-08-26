## 思路
乘法原理。将r的加起来，b的加起来。乘一下。取个模即可
~~~python
n = int(input())
a = list(map(int , input().split()))
s = input()
x = 0
y = 0
for i in range (n):
	if s[i] == 'R':
		x += a[i]
	else:
		y += a[i]
mod = 1000000007
x %= mod
y %= mod
print (x * y % mod)

~~~