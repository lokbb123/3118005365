# -*- coding: utf-8 -*-
"""
本代码主要使用MinHash算法实现文章查重功能，以下是对MinHash算法的简介
MinHash算法是LSH(Locality Sensitive Hashing，局部敏感哈希)中的一种，主要用来判断两个集合之间的相似性，适用于数据量大的集合
MinHash算法的实现流程一般为，将文档划分成子字符串，再利用哈希函数构建签名，最后对比签名从而获得相似度
"""


# 正则包
import re
# 自然语言处理包
import jieba
import jieba.analyse
# html 包
import html
# 数据集处理包
from datasketch import MinHash
import sys   # 从命令行获取参数包

class MinHashSimilarity(object):
    """
    MinHash算法
    """
    def __init__(self, content_x1, content_y2):
        self.s1 = content_x1
        self.s2 = content_y2

    @staticmethod
    def extract_keyword(content):  # 提取关键词
        # 正则过滤 html 标签
        re_exp = re.compile(r'(<style>.*?</style>)|(<[^>]+>)', re.S)
        content = re_exp.sub(' ', content)
        # html 转义符实体化
        content = html.unescape(content)
        # 切割
        seg = [i for i in jieba.cut(content, cut_all=True) if i != '']
        # 提取关键词
        keywords = jieba.analyse.extract_tags("|".join(seg), topK=200, withWeight=False)
        return keywords

    def main(self):
        # 去除停用词
        # jieba.analyse.set_stop_words('./files/stopwords.txt')

        # MinHash计算
        m1, m2 = MinHash(), MinHash()
        # 提取关键词
        s1 = self.extract_keyword(self.s1)
        s2 = self.extract_keyword(self.s2)

        for data in s1:
            m1.update(data.encode('utf8'))
        for data in s2:
            m2.update(data.encode('utf8'))

        return m1.jaccard(m2)


# 测试
if __name__ == '__main__':
    article1_address = sys.argv[1] # 利用sys库，使程序可以从命令行获得原文地址参数
    article2_address = sys.argv[2] # 利用sys库，使程序可以从命令行获得抄袭文本地址参数
    answer_address = sys.argv[3] # 利用sys库，使程序可以从命令行获得输出答案地址参数
    with open(article1_address, 'r') as x, open(article2_address, 'r') as y:
        content_x = x.read()
        content_y = y.read()
        similarity = MinHashSimilarity(content_x, content_y)
        similarity = similarity.main()
        with open(answer_address, 'w') as f:
            f.write('相似度: %.2f%%' % (similarity*100))

