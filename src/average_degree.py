#!/usr/bin/env python

from __future__ import division
from graph2 import Graph
import json
import os
import pdb
import logging
import operator
from datetime import datetime
from collections import OrderedDict
import sys

def average_degree_graph(graph):
    """get average degree of a graph object"""
    average_degree = '0.00'
    edges = float(len(graph.edges()))
    no_vertices = float(len(graph.vertices()))
    if no_vertices != 0:
        average_degree = round(2*edges/no_vertices, 2)
        # print '%.2f' % average_degree
    # print 'res:', edges, no_vertices, average_degree
    return '%.2f' % average_degree

def main():
    try:
        with open(sys.argv[1], 'r') as tweets, open (sys.argv[2], 'w') as output:
            # make a pretty global dictionary to store time and hashtag info
            hashtag_dict = OrderedDict()
            graph = Graph()
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
                        if time_last_tweet is None or len(hashtag_dict.keys()) == 0:
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
                                        if 'text' in hashtag:
                                            # encode() turns unicode to string
                                            tag = hashtag['text'].encode('utf-8').strip()
                                            hashtag_list.append(tag)
                                    # update hashtag_dict with tweet having at least 2 unique tags
                                    if len(set(hashtag_list)) > 1:
                                        hashtag_dict[created_at] = hashtag_list
                        # remove the tweets more than 60 second older than the current tweet
                        for k in sorted(hashtag_dict.keys()):
                            time_elapsed = datetime.strptime(created_at.encode('utf-8'), "%a %b %d %H:%M:%S +0000 %Y") - datetime.strptime(k.encode('utf-8'),"%a %b %d %H:%M:%S +0000 %Y")
                            if time_elapsed.total_seconds() > 60:
                                del hashtag_dict[k]
                            else:
                                break
                        # finally, fill the graph, and derive average degree
                        for k in hashtag_dict:
                            for tag in hashtag_dict[k]:
                                graph.add_vertex(tag)
                            length = len(hashtag_dict[k])
                            for start in range(length - 1):
                                for end in range(start+1, length):
                                    graph.add_edge((hashtag_dict[k][start], hashtag_dict[k][end]))
                            result = average_degree_graph(graph)
                            print result
                            output.write(str(result) + '\n')
                        continue

    except IOError as err:
        print 'File error:', str(err)

if __name__ == '__main__':
    main()
