import argparse
import re
import json
import pandas as pd
from nltk import RegexpTokenizer
import os

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, '..', 'data')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input')
    parser.add_argument('-o', '--output')
    parser.add_argument('-v', '--verbose', action='store_true')

    args = parser.parse_args()

    df = pd.read_csv(args.input, sep='\t')
    df['metrics'] = [json.loads(s) for s in df['metrics']]

    log = '-'*20 + 'statistics' + '-'*20 + '\n'
    log += df.groupby('coding')['id'].count().reset_index(name='count').to_string(index=False) + '\n\n'
    log += df.groupby('sentiment')['id'].count().reset_index(name='count').to_string(index=False) + '\n'
    log += f'total tweets: {len(df.index)}' + '\n'

    if args.verbose:
        print(log)

    # lower, remove numbers and links and tokenize
    tokenizer = RegexpTokenizer(r'\w+') # remove punctuations
    df['tweet'] = [re.sub(r'\bhttps\S*\b', '', s.lower()) for s in df['tweet']]
    df['tweet'] = [re.sub(r'\d', ' ', s) for s in df['tweet']]
    df['tweet'] = [tokenizer.tokenize(s) for s in df['tweet']]
    
    # remove stopwords
    stop_words = set()
    with open(os.path.join(DATA_DIR, 'stopwords.txt')) as f:
        for line in f:
            if not line.startswith('#'):
                stop_words.add(line.strip('\n'))
    
    df['tweet'] = [[token for token in l if token not in stop_words] for l in df['tweet']]
    
    # tf-idf(w, tweet, script) = tf(w, tweet) x idf(w, script)
    # tf(w, tweet) = the number of times tweet contains the word w
    # idf(w, script) = log [(total number of tweets) /(number of tweets that use the word w)]

    # idf
    total_word_count = {}
    sample_size = len(df.index) # 10000
    tweets = df['tweet'].tolist()
    # print(tweets[:3])
    for tweet in tweets:
        pass


    # by topic
    for topic in range(1,7):
        df_topic = df[df['coding'] == topic]
    

    # l = []
    # with open(args.input, encoding='utf-8') as f:
    #     with open(args.output, 'w', encoding='utf-8') as o:
    #         for line in f:
    #             line = line.split('\t')
    #             if not line[2]:
    #                 print(line)
    #                 print(line[2])
    #                 return
    #             text = line[3]
    #             text = re.sub(r'\bhttps:.*\b', '', text)
    #             text = re.sub(r'\s+', ' ', text)
    #             try:
    #                 metrics = json.loads(line[2])
    #                 likes = metrics['like_count']
    #                 l.append((line[0], text, likes))
    #             # re.sub(r'\W+', ' ', text)
    #             # words = text.split()
    #             # o.write(text+'\n\n')

    #             except:
    #                 # print(line)
                    
    #                 print(line[2])
    #         l.sort(key=lambda x: x[2], reverse=True)
    #         top10 = l[:10]
    #         d = []
    #         for x in top10:
    #             d.append({'id':x[0], 'text':x[1], 'likes':x[2]})
    #         json.dump(d,o)
            


if __name__ == '__main__':
    main()
