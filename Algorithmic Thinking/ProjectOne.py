"""
Three example directed graphs are given as dictionary constants

The 3 functions do the following
1) make a complete n - 1 directed graph with no self loops represented as an adjacency list
2) computes the indegrees of each node in adjacency list
3) computes the unnormalized distribution of the in-degrees of the graph
"""

EX_GRAPH0 = {0: set([1,2]), 1: set([]), 2: set([])}
EX_GRAPH1 = {0: set([1,4,5]), 1: set([2,6]), 2: set([3]), 3: set([0]), 4: set([1]), 5: set([2]), 6: set([])}
EX_GRAPH2 ={0: set([1,4,5]), 1: set([2,6]), 2: set([3,7]), 3: set([7]), 4: set([1]), 5: set([2]), 6: set([]), 7: set([3]), 8: set([1,2]), 9: set([0,3,4,5,6,7])}
# EX_GRAPH3 = {'cat': set(['monkey', 'dog']), 'dog': set([]), 'monkey': set([])}

def make_complete_graph(num_nodes):
    """
    make a complete n - 1 directed graph with no self loops represented as an adjacency list
    """
    adj_list = {};

    if num_nodes < 0:
        return adj_list;

    for val in range(num_nodes):
        adj_list[val] = set([])

        for key in range(num_nodes):
            if val != key:
                adj_list[val].add(key);

    return adj_list;

def compute_in_degrees(digraph):
    """
    computes the indegrees of each node in adjacency list
    """
    indegrees = {};

    for node in digraph.keys():
        # print node
        indegrees[node] = 0;

    for node in digraph.keys():
        for neighbor in digraph[node]:
            indegrees[neighbor] = indegrees[neighbor] + 1;

    return indegrees

def in_degree_distribution(digraph):
    """
    computes the unnormalized distribution of the in-degrees of the graph
    """
    indegrees = compute_in_degrees(digraph);
    degree_distribution = {}

    for indegree in indegrees.values():
        if indegree not in degree_distribution.keys():
            degree_distribution[indegree] = 0;

        degree_distribution[indegree] = degree_distribution[indegree] + 1;

    return degree_distribution

