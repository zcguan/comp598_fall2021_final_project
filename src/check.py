import os.path as osp
import pandas as pd

BASE_DIR = osp.dirname(__file__)
DATA_DIR = osp.join(BASE_DIR, '..', 'data')

annotation = osp.join(DATA_DIR, 'annotation_tweets.tsv')
remain = osp.join(DATA_DIR, 'remains.tsv')

df = pd.read_csv(annotation, sep='\t')

print(df[df['sentiment'].isnull() & df['coding'].notnull()])

print(df.groupby('coding')['id'].count().reset_index(name='count'))
print(df.groupby('sentiment')['id'].count().reset_index(name='count'))
df[df['coding'].isnull()].to_csv(remain, sep='\t', columns=['id', 'tweet'])


print(len(df[df['coding'].notnull()].index))
# df['id'] = [len(str(s)) for s in df['id']]
# print(df[df['id'] > len('1463295723978563588')])

print(len(df[df['sentiment'].notnull()].index))
