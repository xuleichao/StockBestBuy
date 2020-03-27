import pycrfsuite as crfs


def feature1(raw_feature):
    '''将输入的交易数据转换为crf特征'''
    up_ratio = raw_feature[0]
    down_ratio = raw_feature[1]
    middle_ratio = raw_feature[1]
    feature = {'up_ratio': up_ratio,
               'down_ratio': down_ratio,
               'middle_ratio': middle_ratio}
    return feature