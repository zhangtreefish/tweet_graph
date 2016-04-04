from __future__ import division
from graph2 import Graph
import json
import os
import pdb
import logging
import operator
from datetime import datetime
from collections import OrderedDict


def average_degree(graph):
    """get average degree given a graph object"""
    ds = graph.degree_sequence()
    total_degrees = sum(ds)
    no_vertices = len(ds)
    if no_vertices != 0:
        average_degree = round(total_degrees/no_vertices,2)
        return '%.2f' % average_degree

# test the method with a sample Graph object
g_no_loop = { "a" : ["d"],
              "b" : ["c"],
              "c" : ["b", "d", "e"],
              "d" : ["a", "c"],
              "e" : ["c"],
              "f" : []
            }

graph_test = Graph(g_no_loop)
result = average_degree(graph_test)

try:
    with open('./tweet_input/tweets.txt', 'r') as tweets, open ('./tweet_output/output.txt', 'w') as output:
        # make a pretty global dictionary to store time and hashtag info
        hashtag_dict = OrderedDict()
        time_last_tweet = None
        while True:
            # read each tweet (per line in the .txt file)
            tweet = tweets.readline().decode('utf-8')
            if not tweet:
                break;
            else:
                tweet_json = json.loads(tweet) # dict object
                if 'created_at' in tweet_json: # needed to address keyError
                    # get the time of the tweet
                    created_at = tweet_json['created_at']
                    # get the time of the last tweet
                    if time_last_tweet is None:
                        time_last_tweet = created_at
                    else:
                        time_last_tweet = hashtag_dict.keys()[-1]
                    # ensure to only address tweets not over 60 seconds older than the last
                    time_current = datetime.strptime(created_at.encode('utf-8'), "%a %b %d %H:%M:%S +0000 %Y")
                    time_last = datetime.strptime(time_last_tweet.encode('utf-8'), "%a %b %d %H:%M:%S +0000 %Y")
                    time_delta = time_current - time_last
                    if time_delta.total_seconds() > - 60:
                        if 'entities' in tweet_json:
                            if 'hashtags' in tweet_json['entities']:
                                hashtags = tweet_json['entities']['hashtags']
                                hashtag_list = []
                                # make a list with the hashtags
                                for hashtag in hashtags:
                                    # encode() turns unicode to string
                                    tag = hashtag['text'].encode('utf-8').strip()
                                    hashtag_list.append(tag)
                                # store the time and tags as key:value pairs in the dictionary
                                hashtag_dict[created_at] = hashtag_list
                                # print created_at, hashtag_dict[created_at]
                    # remove the tweets more than 60 second older than the current tweet
                    for k in hashtag_dict.keys():
                        time_elapsed = datetime.strptime(created_at.encode('utf-8'), "%a %b %d %H:%M:%S +0000 %Y") - datetime.strptime(k.encode('utf-8'),"%a %b %d %H:%M:%S +0000 %Y")
                        if time_elapsed.total_seconds() > 60:
                            del hashtag_dict[k]
                    # finally, all the preparation leads to: average degree!
                    if hashtag_dict:
                        hashtag_graph = Graph()
                        # print 'dict[created_at]', hashtag_dict[created_at]
                        hashtag_graph.add_edge(hashtag_dict[created_at])
                        result = average_degree(hashtag_graph)
                        print result
                        output.write(str(result) + '\n')
                    continue

except IOError as err:
    print 'File error:', str(err)
