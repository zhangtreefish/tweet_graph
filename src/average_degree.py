from __future__ import division
from graph2 import Graph

g_no_loop = { "a" : ["d"],
                  "b" : ["c"],
                  "c" : ["b", "d", "e"],
                  "d" : ["a", "c"],
                  "e" : ["c"],
                  "f" : []
                }

graph = Graph(g_no_loop)

ds = graph.degree_sequence()
total_degrees = sum(ds)
print 'total_degrees:', total_degrees
no_vertices = len(ds)
print 'no_vertices:', no_vertices
average_degree = round(total_degrees/no_vertices,2)
print 'average_degree:', average_degree
