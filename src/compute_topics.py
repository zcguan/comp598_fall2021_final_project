import pandas as pd
import os
import os.path as osp
import json
import argparse
import math


def json_to_dict(in_file):

    with open(in_file,'r') as f:
        data=json.load(f)
    return data

def tf(w,topic,topic_wc):
    return topic_wc[topic][w]

def idf(w,topic_wc):

    #get number of topics that use word w
    num_used = 0

    for topic in topic_wc:
        if w in topic_wc[topic]:
            num_used+=1

    return math.log(6/num_used)


def tf_idf(w,topic,topic_wc):
    return tf(w,topic,topic_wc) * idf(w,topic_wc)

def get_tfidf_list(topic_wc):

    topic_tfidf = {str(n):[] for n in range(1,7) }

    #topic_tfidf is dictionary with keys topic name and values are tuple of word and its tfidf score
    for topic in topic_wc:
        for word in topic_wc[topic]:
            topic_tfidf[topic].append((word,tf_idf(word,topic,topic_wc)))

    #sort lists in topic_tfidf in descendinng order
    for topic in topic_tfidf:
        topic_tfidf[topic].sort(key=lambda x:x[1] , reverse=True)

    return topic_tfidf

def dict_to_output(topic_tfidf):
    dict_to_print = {}
    for topic in topic_tfidf:
        dict_to_print[topic]= [x for x in topic_tfidf[topic][0:10]]

    return dict_to_print

def print_output(d):
    json_obj = json.dumps(d,indent=3)
    print(json_obj)

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--topic_counts')

    args = parser.parse_args()

    topic_wc = json_to_dict(args.topic_counts)

    topic_tfidf = get_tfidf_list(topic_wc)

    dict_to_print = dict_to_output(topic_tfidf)

    print_output(dict_to_print)


if __name__=="__main__":
    main()

