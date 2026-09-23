import sys


def _skip_space(text: str, i: int) -> int:
    while i < len(text) and text[i] in " \t\n\r":
        i += 1
    return i


def parse_input(text: str):
    """解析与原题样例一致的输入：["cmd",...],"prefix\""""
    text = text.strip()
    i = 0
    i = _skip_space(text, i)
    if not text or text[i] != "[":
        return [], ""
    i += 1
    commands = []
    while True:
        i = _skip_space(text, i)
        if i < len(text) and text[i] == "]":
            i += 1
            break
        if i >= len(text) or text[i] != '"':
            break
        i += 1
        start = i
        while i < len(text) and text[i] != '"':
            i += 1
        commands.append(text[start:i])
        if i < len(text) and text[i] == '"':
            i += 1
        i = _skip_space(text, i)
        if i < len(text) and text[i] == "]":
            i += 1
            break
        if i < len(text) and text[i] == ",":
            i += 1
            continue
        break
    i = _skip_space(text, i)
    prefix = ""
    if i < len(text) and text[i] == ",":
        i += 1
        i = _skip_space(text, i)
        if i < len(text) and text[i] == '"':
            i += 1
            start = i
            while i < len(text) and text[i] != '"':
                i += 1
            prefix = text[start:i]
    return commands, prefix


def format_output(arr):
    """输出格式与样例一致：["a","b"]"""
    parts = ['"' + x + '"' for x in arr]
    return "[" + ",".join(parts) + "]"


def main():
    commands, prefix = parse_input(sys.stdin.read())
    ans = Solution().FindNextKeywords(commands, prefix)
    print(format_output(ans))


if __name__ == "__main__":
    main()
