import pandas as pd
from config.db_config import db_config
from utils.impdataframe import engine

feature_path = '../dataSets/feature/省广集团.txt'

# data = open(feature_path, 'r', encoding='utf-8').readlines()
# data = [i.strip().split(',') for i in data]

df = pd.read_csv(feature_path, header=None)
df[0] = pd.to_datetime(df[0])
df_tag_data = pd.read_sql('select * from stock_tagging_data', con=engine)
merge_result = pd.merge(df, df_tag_data, how='right', left_on=0, right_on='date_time')
shift_tag = merge_result[['tagging']].shift(-1, axis='index')
feature_info_df = merge_result[[1, 2, 3, 'tagging']]
feature_info_df[:-1].to_csv('./feature_省广_with_tagging.txt', index=False, header=False, sep='\t')
pass