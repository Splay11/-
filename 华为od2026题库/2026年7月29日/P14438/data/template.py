import ast
import sys

# 读取整行输入
line = sys.stdin.read().strip()

# 解析 R
c1 = line.find(',')
R = int(line[:c1].strip())

# 解析 G
rest1 = line[c1 + 1:]
c2 = rest1.find(',')
G = int(rest1[:c2].strip())

# 剩余部分: [E,S,W,N],[0,1,3,6]
rest2 = rest1[c2 + 1:]
# 找 ] 后的逗号切分两个列表
close_bracket = rest2.find('],[')
dirs_str = rest2[1:close_bracket]   # E,S,W,N (不包含 ']')
times_str = rest2[close_bracket + 3:-1]  # 0,1,3,6

# 解析方向列表
directions = [s.strip() for s in dirs_str.split(',') if s.strip()]

# 解析到达时间列表
arrivalTimes = [int(s.strip()) for s in times_str.split(',') if s.strip()]

# 调用用户代码
result = Solution().intersectionWaitingTime(R, G, directions, arrivalTimes)
print(f"[{result[0]},{result[1]}]")
