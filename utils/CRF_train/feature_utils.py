'''
Created on 2020年4月20日
特征抽取函数 CRF
@author: 闪闪的红星
'''
import re
import pandas as pd
import math
import pycrfsuite as crfs

# 定义需要5天的股票K线数据, 预测未来的走势
def feature(all_feature):
    '''将将输入的交易数据转换为crf特征'''
    raw_feature = all_feature[-1]
    up_ratio = raw_feature[0]
    down_ratio = raw_feature[1]
    middle_ratio = raw_feature[2]
    features = ['up_ratio=' + up_ratio,
               'down_ratio=' + down_ratio,
               'middle_ratio=' + middle_ratio]

    length = len(all_feature)
    for i in range(length-1):
        back_idx = length - i -1
        raw_feature_new = all_feature[i]
        up_ratio_new = raw_feature_new[0]
        down_ratio_new = raw_feature_new[1]
        middle_ratio_new = raw_feature_new[2]
        feature_item = [('-{c}:up_ratio=' + up_ratio_new).format(c=back_idx),
                        ('-{c}:down_ratio=' + down_ratio_new).format(c=back_idx),
                        ('-{c}:middle_ratio=' + middle_ratio_new).format(c=back_idx)]
        features.extend(feature_item)
    return features

def get_train_data(path='../feature_省广_with_tagging.txt', split_num=5):
    # split_num: 多少个特征为一个序列，即窗口大小
    f = open(path, 'r', encoding='utf-8').readlines()
    data = [i.strip().split('\t') for i in f][:]
    return data
    feature_result_split = []
    all_chunk = math.ceil(len(data) / split_num)
    count = 0
    while len(feature_result_split) < all_chunk:
        end_count = count + 5
        sub_seq = data[count: end_count]
        feature_result_split.append(sub_seq)
        count += 5
    return feature_result_split

def Train(X, y_label, model_path='./model/crf-stock-model.crfsuite'):
    # 模型训练
    trainer = crfs.Trainer(verbose=False)
    for x, y in zip(X, y_label):
        trainer.append(x, y)
    trainer.set_params({
        'c1': 1.0,  # coefficient for L1 penalty
        'c2': 1e-3,  # coefficient for L2 penalty
        'max_iterations': 50,  # stop earlier
        # include transitions that are possible, but not observed
        'feature.possible_transitions': True
    })
    trainer.train(model_path)

def feed_data_and_train(path='../feature_省广_with_tagging.txt', split_num=5):
    data = get_train_data(path)
    data = data[: 1000]
    first_idx = lambda x: 0 if x < 0 else x

    features = [[feature(data[first_idx(i+1-split_num): i+1])] for i in range(len(data))]
    X = features
    y_label = [[i[-1]] for i in data]
    pass
    Train(X, y_label, model_path='./model/crf-stock-model.crfsuite')

def get_tagger(model_path='./model/crf-stock-model.crfsuite'):
    tagger = crfs.Tagger()
    tagger.open(model_path)
    return tagger

tagger = get_tagger()
def predict(data, split_num=5):
    first_idx = lambda x: 0 if x < 0 else x
    new_feature = [[feature(data[first_idx(i+1-split_num): i+1])] for i in range(len(data))]
    result = []
    for i in new_feature:
        result.append(tagger.tag(i)[0])
    return result

if __name__ == '__main__':
    # items = [['好', '2', '3'], ['好', '2', '3'], ['好', '2', '3'], ['e', '=', '5']]
    # b = feature(items)
    # print(b)
    # feed_data_and_train(path='../feature_省广_with_tagging.txt')
    # pass
    # # test
    # data = get_train_data()[1000:]
    # print(predict(data))
    feature_file = '../../dataSets/feature/省广集团.txt'
    data = pd.read_csv(feature_file, header=None)
    data_for_predict = [i[1:] for i in data.values]
    result = predict(data_for_predict)
    df_result = pd.DataFrame(result)
    data['是否入手'] = df_result[0].shift(1, axis='index')
    data[[0, '是否入手']].to_excel('../../对历史数据预测结果.xlsx', index=False)
    pass

