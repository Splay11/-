print(sum([1 if i % 10 == sum([int(x) for x in str(i)]) % 10 else 0 for i in range(1 , int(input()) + 1)]))
