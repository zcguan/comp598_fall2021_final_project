import argparse
import re
import json
import pandas as pd
import nltk
from nltk import RegexpTokenizer
from nltk.corpus import stopwords
import os
import os.path as osp

nltk.download('stopwords')

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, '..', 'data')

'''counts number of occurence of each word in a tweet'''
def count_words_topic(tweet):
    
    word_count={}
    #tweet passed in as list of words
    for word in tweet:

        if word.lower() not in word_count:
            word_count[word.lower()]=1
        else:
            word_count[word.lower()]+=1

    return word_count


'''get counts of all words by topic'''
def get_totals(df):

    topic_wc = {n:{} for n in range(1,7)}

    for topic,tweet in zip(df['coding'],df['tweet']):

        #get num appearences of each word in tweet
        word_counts = count_words_topic(tweet)

        #all words in word_counts are lowercase

        #update topic_wc with count values of words in act
        for word in word_counts:
            if word not in topic_wc[int(topic)]:
                topic_wc[int(topic)][word] = word_counts[word]
            else:
                topic_wc[int(topic)][word] += word_counts[word]
    return topic_wc

'''keeps words that appear more than 5 times across all tweets'''
def words_more5(topic_wc):
    
    sus_words = {}
    for topic in topic_wc:
        for word in topic_wc[topic]:
            if topic_wc[topic][word] < 5:
                if word not in sus_words:
                    sus_words[word] = topic_wc[topic][word]
                else:
                    sus_words[word] += topic_wc[topic][word]

    #remove words from topic_wc if appear less than 5 times
    for word in sus_words:
        if sus_words[word] < 5:
            for topic in topic_wc:
                if word in topic_wc[topic]:
                    topic_wc[topic].pop(word)
    return topic_wc

'''calculates average sentiment for each topic'''
def get_avg_sentiment(df):

    topic_wc = {n:{"count":0,"sentiment":0} for n in range(1,7)}

    for topic,sentiment in zip(df['coding'],df['sentiment']):

        topic_wc[int(topic)]["sentiment"]+= sentiment
        topic_wc[int(topic)]["count"]+= 1

    avg_sentiment = {n:0 for n in range(1,7)}
    for topic in avg_sentiment:
        avg_sentiment[topic] = topic_wc[topic]["sentiment"] / topic_wc[int(topic)]["count"]

    return avg_sentiment


def to_json(out_file,in_dict):
    dir_name,file_name = osp.split(out_file)

    if dir_name != '':
        try:
            os.makedirs(dir_name)
        except OSError as error:
           pass

    with open(out_file,'w') as f:
            json.dump(in_dict,f,indent=2)



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input')
    parser.add_argument('-o', '--output')

    args = parser.parse_args()

    df = pd.read_csv(args.input, sep='\t')
    df['metrics'] = [json.loads(s) for s in df['metrics']]

    log = '-'*20 + 'statistics' + '-'*20 + '\n'
    log += df.groupby('coding')['id'].count().reset_index(name='count').to_string(index=False) + '\n\n'
    log += df.groupby('sentiment')['id'].count().reset_index(name='count').to_string(index=False) + '\n'
    log += f'total tweets: {len(df.index)}' + '\n'

    # lower, remove numbers and links and tokenize
    tokenizer = RegexpTokenizer(r'\w+') # remove punctuations
    df['tweet'] = [re.sub(r'\bhttps\S*\b', '', s.lower()) for s in df['tweet']]
    df['tweet'] = [re.sub(r'\d', ' ', s) for s in df['tweet']]
    df['tweet'] = [tokenizer.tokenize(s) for s in df['tweet']]
    
    # remove stopwords
    stop_words = set(stopwords.words('english'))
    with open(os.path.join(DATA_DIR, 'stopwords.txt')) as f:
        for line in f:
            if not line.startswith('#'):
                stop_words.add(line.strip('\n'))
    
    df['tweet'] = [[token for token in l if token not in stop_words] for l in df['tweet']]

    # # by topic
    for topic in range(1,7):
        df_topic = df[df['coding'] == topic]
        log += '-'*20 + f'topic{topic}' + '-'*20 + '\n'
        log += df_topic.groupby('coding')['id'].count().reset_index(name='count').to_string(index=False) + '\n\n'
        log += df_topic.groupby('sentiment')['id'].count().reset_index(name='count').to_string(index=False) + '\n'
        log += f'total tweets: {len(df_topic.index)}' + '\n'

    print(log)
    
    #get word count for each topic (all words must appear at least 5 times over all tweets)
    topic_wc = get_totals(df)
    topic_wc = words_more5(topic_wc)

    #output to json file
    to_json(args.output,topic_wc)
    
    print(f"Average Sentiment score for each topic: \n {get_avg_sentiment(df)}")
if __name__ == '__main__':
    main()
