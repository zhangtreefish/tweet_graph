#!/usr/bin/env python

from __future__ import division
#from graph2 import Graph
import json
import os
import pdb
import logging
import operator
from datetime import datetime
from collections import OrderedDict
import sys

class Graph(object):

    def __init__(self, graph_dict={}):
        """ initializes a graph object """
        self.__graph_dict = graph_dict

    def vertices(self):
        """ returns the vertices of a graph """
        return list(self.__graph_dict.keys())

    def edges(self):
        """ returns the edges of a graph """
        return self.__generate_edges()

    def add_vertex(self, vertex):
        """ If the vertex "vertex" is not in
            self.__graph_dict, a key "vertex" with an empty
            list as a value is added to the dictionary.
            Otherwise nothing has to be done.
        """
        if vertex not in self.__graph_dict:
            self.__graph_dict[vertex] = []

    def add_edge(self, edge):
        """ assumes that edge is of type set, tuple or list;
            between two vertices can be multiple edges!
            [Edited by this author: if edge]
        """
        if edge:
            edge = set(edge)
            vertex1 = edge.pop()
            vertex2 = None
            if edge:
                # not a loop
                vertex2 = edge.pop()
            # else:
            #     # a loop
            #     vertex2 = vertex1
            if vertex1 in self.__graph_dict:
                self.__graph_dict[vertex1].append(vertex2)
            else:
                self.__graph_dict[vertex1] = [vertex2]

    def __generate_edges(self):
        """ A static method generating the edges of the
            graph "graph". Edges are represented as sets
            with one (a loop back to the vertex) or two
            vertices
        """
        edges = []
        for vertex in self.__graph_dict:
            for neighbour in self.__graph_dict[vertex]:
                if {neighbour, vertex} not in edges:
                    edges.append({vertex, neighbour})
        return edges

def average_degree_graph(graph):
    """get average degree of a graph object"""
    average_degree = 0.00
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
            # graph = Graph()
            time_last_tweet = None
            for line in tweets:
                # read each tweet (per line in the .txt file)
                tweet = line.decode('utf-8')
                # if not tweet:
                #     break;
                # else:
                tweet_json = json.loads(tweet) # dict object
                if 'created_at' in tweet_json: # needed to address keyError
                    # get the time of the tweet
                    created_at = datetime.strptime(tweet_json['created_at'].encode('utf-8'), "%a %b %d %H:%M:%S +0000 %Y")
                    # get the time of the last tweet
                    if time_last_tweet is None or len(hashtag_dict.keys()) == 0:
                        time_last_tweet = created_at
                    else:
                        time_last_tweet = hashtag_dict.keys()[-1]
                    # ensure to only address tweets not over 60 seconds older than the last
                    # time_current = datetime.strptime(created_at.encode('utf-8'), "%a %b %d %H:%M:%S +0000 %Y")
                    # time_last = datetime.strptime(time_last_tweet.encode('utf-8'), "%a %b %d %H:%M:%S +0000 %Y")
                    time_delta = created_at - time_last_tweet
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

                                # TODO: list comprehension below raises empty set error
                                #
                                # if 'text' in hashtags[hashtag]:
                                #     hashtag_list = [i['text'].encode('utf-8').strip() for i in hashtags]
                                # update hashtag_dict if at least 2 tags
                                if len(set(hashtag_list)) > 1:
                                    hashtag_dict[created_at] = hashtag_list
                                    # print 'hashtag_dict_before_remove', hashtag_dict
                                    # for tag in hashtag_list:
                                    #     graph.add_vertex(tag)
                                    # for start in range(len(hashtag_list) - 1):
                                    #     for end in range(start+1, len(hashtag_list)):
                                    #         graph.add_edge((hashtag_list[start], hashtag_list[end]))
                                    #         graph.add_edge((hashtag_list[end], hashtag_list[start]))
                    else:
                        continue
                    # remove the tweets more than 60 second older than the current tweet
                    for k in sorted(hashtag_dict.keys()):
                        time_elapsed = created_at - k
                        if time_elapsed.total_seconds() > 60:
                            del hashtag_dict[k]
                        else:
                            break
                    # finally, initialize the graph, and derive average degree
                    graph = Graph()
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
