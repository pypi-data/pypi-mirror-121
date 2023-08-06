import string

strList = []
enbiao = r""",.;?:!．"""
zhbiao = r"""，。、；？：！"""

en_zh_dict = {',': '，', '.': '。', '?': '？', ';': '；', ':': '：', '!': '！', '．': '。',
              '，': ',', '。': '.', '、': ',', '？': '?', '；': ';', '：': ':', '！': '!'}


def is_chinese(word: str) -> bool:
    """ 是否是中文 """

    if not '\u4e00' <= word <= '\u9fa5':
        return False
    else:
        return True


def parse_line(line: list) -> str:
    """ 处理每一行 """

    for i, word in enumerate(line):
        if (word in zhbiao) and (line[i-1] in string.ascii_letters):
            line[i] = en_zh_dict[word]
            print(line[i-1], line[i], word)
        elif (word in enbiao) and (is_chinese(line[i-1])):
            line[i] = en_zh_dict[word]
            print(line[i-1], line[i], word)
        else:
            pass
    lined = ''.join(line)
    return lined


def range_lines(lines: list) -> list:
    """ 处理字符串列表 """

    lined = []
    for line in lines:
        lined.append(parse_line(list(line)))
    return lined


""" with open('test.txt', 'rt', encoding='UTF-8') as f:
    lines = f.readlines()
    lined = []
    for line in lines:
        # print(line)
        lined.append(parse_line(list(line)))
    with open('result.txt', 'wt', encoding='UTF-8') as f2:
        f2.writelines(lined) """


def main():
    print("hello")


# __all__ = ['range_lines']


if __name__ == '__main__':
    main()
