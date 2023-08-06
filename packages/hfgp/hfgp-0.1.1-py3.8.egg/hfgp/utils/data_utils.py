# -*- coding: utf-8 -*-
# @Date    : 2021/9/16 15:18
# @Author  : stellahong (stellahong@fuzhi.ai)
# @Desc    :
from sentence_transformers import InputExample

def convert2clssample(x, y):
    """
    给定输入样本array, 转化成对应分类样本数据
    :return:
    """
    samples = []
    for x, y in zip(x, y):
        samples.append(InputExample(texts=[" ".join(x.split(" "))[:]], label=y))
    return samples
