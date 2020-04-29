'''提取数据特征，拆分数据集'''
# 数据处理

import numpy as np
import pandas as pd

def random_tag(shape):
    # 随机标注
    res = np.random.randint(2, size=shape)
    return res

datasets_file = '../../dataSets/feature/省广集团.txt'
df = pd.read_csv(datasets_file, header=None)
df.columns = ["日期", '上比例', "下比例", '中比例']
df['日期'] = pd.to_datetime(df['日期'], format="%m/%d/%Y")
df['target'] = pd.DataFrame(random_tag(df.shape[0]))[0]
# 数据分割 8：1：1
train_sets_shape = int(df.shape[0] * 8 / 10)
test_sets_shape = int(df.shape[0] * 1 / 10)
train_index = train_sets_shape
test_index = test_sets_shape + train_index
train_df = df[: train_index]
test_df = df[train_index + 1: test_index]
valid_df = df[test_index:]
pass