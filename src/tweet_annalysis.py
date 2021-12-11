import argparse
import re
import json
import pandas as pd

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

    # tf-idf(w, tweet, script) = tf(w, tweet) x idf(w, script)
    # tf(w, tweet) = the number of times tweet contains the word w
    # idf(w, script) = log [(total number of tweets) /(number of tweets that use the word w)]

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
