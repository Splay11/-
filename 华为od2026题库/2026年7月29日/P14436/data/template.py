import sys

line = sys.stdin.read().strip()
comma = line.find(',')
n = int(line[:comma])
arr_str = line[comma + 1:].strip()
if arr_str == '[]':
    energies = []
else:
    energies = list(map(int, arr_str[1:-1].split(',')))

result = Solution().energyCollision(energies)
print('[' + ','.join(map(str, result)) + ']')
