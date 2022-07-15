# README
> created by CST12 张天祺

# 项目介绍
本项目通过用户目录下的生词本`./collection.txt`文件来生成可以用于复习的单词本文件

约定的参数如下：
```python
1. -n 表示用户希望从自己所选择范围内具体想要复习的单词数量
2. --r 表示用户希望随机选择单词（不输入 --r 则表示不希望随机选择）
3. -s 表示用户希望从第几个单词开始
4. -l 表示用户希望复习的单词范围大小，也即从 start 开始，长度为 length
5. -a 表示用户希望一次性生成多个单词本，参数为amount
```
例如：
`python3 selector.py -n 100 --r -s 20 -l 200 -a 5` 表示希望从生词本的第 20 个单词开始到第 220 个单词结束的范围内随机抽取 100 个生词生成生词本，并生成5次

单词本存放在`./workbook` 路径下，含有翻译完全和未翻译两种。旧的生词本不会被新生成的生词本覆盖

# 项目环境
- 用户需要能保证访问到`translate.google.cn`
- 为保证不出错，请使用`python3.8`及以上环境
- 项目所需要的包：`numpy`,`argparse`, `tqdm`, `googletrans`,其中要保证`googletrans==4.0.0-rc1`或更高
- 搭建虚拟环境以及安装相关包的方式：
```shell
conda create -n summer python=3.8
conda activate summer
pip install numpy
pip install argparse
pip install tqdm
pip install googletrans==4.0.0-rc1
```
