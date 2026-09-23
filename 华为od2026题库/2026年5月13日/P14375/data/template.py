import sys
import ast
import json

def main():
    data = sys.stdin.read().strip()
    if not data:
        return
    nodes, relations, myId, maxHop = ast.literal_eval("(" + data + ")")
    result = Solution().queryFriends(nodes, relations, myId, int(maxHop))
    sys.stdout.write(json.dumps(result, ensure_ascii=False, separators=(",", ":")))

if __name__ == "__main__":
    main()
