### 第二题 ###

import sys

def modify_string(string, k):
    result = []
    seen_chars = set()

    for i, char in enumerate(string):
        if char in seen_chars:
            result.append('-')
        else:
            seen_chars.add(char)
            result.append(char)

        if i >= k:
            seen_chars.discard(string[i - k])

    return ''.join(result)


if __name__ == "__main__":
    args = sys.argv
    if len(args) != 3:
        print("请输入：字符串、数字k")
    elif not args[2].isdigit():
        print("第二个input需为数字")
    else:
        print(modify_string(args[1], int(args[2])))
