import sys
import re
# 读取整份输入，兼容 N,T,{...},{...} 格式
_data = sys.stdin.read().strip()
_nums = list(map(int, re.findall(r'\d+', _data)))

_N = _nums[0]
_T = _nums[1]
_m = (len(_nums) - 2) // 2
_accuracy = _nums[2:2 + _m]
_latency = _nums[2 + _m:2 + 2 * _m]

# 调用用户代码
print(Solution().maxTotalAccuracy(_N, _T, _accuracy, _latency), end="")
