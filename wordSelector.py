import numpy as np
import argparse
from googletrans import Translator
from IPython import embed
from tqdm import tqdm
import os
import re
import sys

def parser_data():
    """
    从命令行读取用户参数
    做出如下约定：
    1. -n 表示用户希望从自己所选择范围内具体想要复习的单词数量
    2. --r 表示用户希望随机选择单词（不输入 --r 则表示不希望随机选择）
    3. -s 表示用户希望从第几个单词开始
    4. -l 表示用户希望复习的单词范围大小，也即从 start 开始，长度为 length
    5. -a 表示用户希望一次翻译多少单词集
    具体的边界条件请查看代码细节
    Returns:
        _type_: _description_
    """
    parser = argparse.ArgumentParser(
        prog="TOELF words reviewer",
        description="choose random or sorted method.",
        allow_abbrev=True,
    )
    parser.add_argument(
        "-n",
        "--num",
        dest="num",
        type=int,
        default=50,
        help="how many words would you like to review",
    )
    parser.add_argument(
        "--r",
        action="store_true",
        dest="random",
        help="if you want to random select, then input --r, otherwise do not",
    )
    parser.add_argument(
        '-s',
        dest="start",
        type=int,
        default=1,
        help='which index to start reading from',
    )
    parser.add_argument(
        '-l',
        dest="length",
        type=int,
        default=100,
        help='how many words would you randomly choose from',
    )
    parser.add_argument(
        '-a',
        dest="amount",
        type=int,
        default=1,
        help='how many wordbook would you like to create'
    )
    args = parser.parse_args()
    return args.random, args.num, args.start, args.length, args.amount

def get_index() -> int:
    """
    使用 os.walk 方法来获取所有单词本的编号，返回单词本的最大编号，即 index
    Returns:
        index: 单词本的最大编号
    """
    try:
        for _, __, files in os.walk("./wordbook"):
            index = 0
            for file in files:
                if file.endswith(".txt"):
                    index = max(
                        index, max([int(each) for each in (re.findall(r"\d+", file))])
                    )
        return index
    except:
        print("Can't find road ./wordbook !")
        sys.exit()

def create_dic(random, num, start, length, _) -> list:
    """
    通过命令行传入的参数对collection.txt进行预处理
    返回一个单词的列表
    Args:
        random ( bool ): 是否生成随机单词本
        num ( int ): 生成单词本所含单词的个数
        start ( int ): 从生词本的第几个单词开始
        length ( int ): 表示用户希望复习的单词范围大小，也即从 start 开始，长度为 length
    """
    with open("./collection.txt", "r", encoding='utf-8') as f:
        words = [line.strip() for line in f]
        while '' in words:
            words.remove('')
    # 处理collection.txt,并除去列表中的空格
        if num > len(words) or num < 1:
            print(f"A wrong size of wordbook! The maximum number of words is {len(words)}.")
            sys.exit()
        if length < num or start > len(words):
            print(f"A wrong range! Please ensure 'length' is larger than 'num', and 'start' is not beyond {len(words)}!")
            sys.exit()
    # 对可能出现的错误输入进行判断
        if random:
            print("You choose random select!")
            if (start + length - 1) > len(words):
                words = words[start-1:]
            else:
                words = words[start-1:start+length-1]
            rng = np.random.default_rng()
            words = rng.choice(words, num, replace=False)
        else:
            words = words[start-1:start+num-1]
    # 按照是否出现random参数来分情况处理列表words
    return words

def create_wordbook(words, index) -> None:
    """
    生成单词本的主函数
    分别生成带翻译版本的和不带翻译版本的
    Args:
        words ( list ):包含单词的列表
        index (_type_): 从 ./wordbook 文件夹下查找所有单词本最大的编号，即 index,将 index + 1 记为当做单词本的编号
    """
    translator = Translator(service_urls=['translate.google.cn'])
    with open(f"./wordbook/untranslated_{index + 1}.txt", "w", encoding='utf-8') as filename:
        for idx, each in enumerate(words):
            filename.write(f"第{idx + 1}词组: {each}\n")

    with open(f"./wordbook/translated_{index + 1}.txt", "w", encoding='utf-8') as filename:
        for idx in tqdm(range(len(words))):
            words_group = words[idx].split(",")
            filename.write(f"第{idx + 1}词组： ")
            for each in words_group:
                try:
                    filename.write(each + ": " + translator.translate(each, dest='zh-CN').text + "\t")
                except:
                    filename.write(each + ": 翻译失败")
            filename.write("\n")
    print("Done!")

if __name__ == "__main__":
    """
    根据-a参数来判断生成单词本的数量
    """
    print(f"Total wordbook number: {parser_data()[4]}")
    for i in range(parser_data()[4]):
        create_wordbook(create_dic(*parser_data()), get_index())
        print(f"Wordbook_{i + 1} created\n")
    
