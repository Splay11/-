import sys
import ast

def main():
    text = sys.stdin.read().strip()
    if not text:
        nums = []
    else:
        nums = ast.literal_eval(text)
    
    ans = Solution().longestBeautifulLanterns(nums)
    print(str(ans).replace(', ',','))

if __name__ == "__main__":
    main()
