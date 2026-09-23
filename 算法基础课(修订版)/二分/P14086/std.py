def find_first_position(a , T):
    n = len(a)
    left , right = 0 , n - 1
    while left <= right:
        mid = (left + right) // 2
        if a[mid] < T:
            left = mid + 1
        else:
            right = mid - 1
    return left + 1 if left <= n - 1 and a[left] == T else -1
def find_last_position(a , T):
    n = len(a)
    left , right = 0 , n - 1
    while left <= right:
        mid = (left + right) // 2
        if a[mid] <= T:
            left = mid + 1
        else:
            right = mid - 1
    return right + 1 if right >= 0 and a[right] == T else -1   
def solve(a , T):
    first = find_first_position(a , T)
    last = find_last_position(a , T)
    return first , last

n , Q = map(int, input().split())
arr = list(map(int, input().split()))
for _ in range(Q):
    T = int(input())
    print(*solve(arr , T))
