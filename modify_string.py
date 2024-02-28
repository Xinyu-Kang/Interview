### 第二题 ###

import sys

def modify_string(string, k):
    char_dict = {}
    str_lst = list(string)
    for i in range(len(str_lst)):
        c = str_lst[i]
        if c in char_dict and i - char_dict[c] < k:
            str_lst[i] = '-'
        char_dict[c] = i
    return "".join(str_lst)


if __name__ == "__main__":
    args = sys.argv
    if len(args) != 3:
        print("请输入：字符串、数字k")
    elif not args[2].isdigit():
        print("第二个input需为数字")
    else:
        print(modify_string(args[1], int(args[2])))
