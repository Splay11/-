import sys
import ast

def split_input(text):
    parts = []
    current = []
    in_quote = False
    escape = False
    for ch in text:
        if escape:
            current.append(ch)
            escape = False
            continue
        if ch == "\\":
            current.append(ch)
            escape = True
            continue
        if ch == '"':
            current.append(ch)
            in_quote = not in_quote
            continue
        if ch == "," and not in_quote:
            parts.append("".join(current).strip())
            current = []
        else:
            current.append(ch)
    parts.append("".join(current).strip())
    return parts


def parse_string_token(token):
    token = token.strip()
    if len(token) >= 2 and token[0] == '"' and token[-1] == '"':
        try:
            value = ast.literal_eval(token)
            if isinstance(value, str):
                return value
        except Exception:
            return token
    return token


def main():
    text = sys.stdin.read()
    parts = split_input(text)

    if len(parts) != 3:
        preorder_str = ""
        inorder_str = ""
        be_deleted_node = "\0"
    else:
        preorder_str = parse_string_token(parts[0])
        inorder_str = parse_string_token(parts[1])
        deleted_token = parse_string_token(parts[2])
        be_deleted_node = deleted_token if len(deleted_token) == 1 else "\0"

    ans = Solution().buildAfterDelete(preorder_str, inorder_str, be_deleted_node)
    if not isinstance(ans, str):
        ans = ""
    print('"' + ans + '"')


if __name__ == "__main__":
    main()
