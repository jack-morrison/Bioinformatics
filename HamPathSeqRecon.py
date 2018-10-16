#!/usr/bin/env python3

#### Jack Morrison
#### Hamiltonian Path Finding for Sequence Reconstruction

import time
from itertools import permutations

def buildGraph(kmers):
    graph = {}
    for i in range(len(kmers)):
        graph[i] = []
        for j in range(len(kmers)):
            if kmers[i][1:] == kmers[j][:-1]:
                graph[i].append(j)

    return graph


## Take a brute force approach, testing all permutations of vertices to see
## if one is a Hamiltonian path through the graph.
def findHamiltonianPathBF(graph, num_vertices):
    v = [i for i in range(num_vertices)]
    for path in permutations(v):
        for i in range(len(path)-1):
            if path[i+1] not in graph[path[i]]:
                break
        else:
            return path
    return []


## Take a branch and bound approach, only extending the path along edges that
## lead to an unvisited vertex. If all vertices are used, a path has been found.
def findHamiltonianPathBB(graph, num_vertices):
    verticesLeft = [i for i in range(num_vertices)]
    path = []
    if SearchTree(graph, path, verticesLeft):
        return result
    else:
        return []


def SearchTree(graph, path, verticesLeft):
    global result
    if len(verticesLeft) == 0:
        result = path
        return True
    for v in verticesLeft:
        if len(path) == 0 or (v in graph[path[-1]]):
            if SearchTree(graph, path+[v], [r for r in verticesLeft if r!=v]):
                return True
    return False



def main():

    ## Two sets of input k-mers
    #kmers = ['ACA','ATT','CAT','CTG','CTT','GCT','TCT','TGA','TGC','TTC','TTG','TTT']
    kmers = ['ATG', 'TGG', 'TGC', 'GTG', 'GGC', 'GCA', 'GCG', 'CGT']
    #kmers = ['ATG', 'ATG']

    print("\n ==> Input k-mers:\n    ", kmers)

    graph = buildGraph(kmers)
    print("\n ==> Graph Structure (Adjacency List):\n    ", graph)

    BFstart = time.time()
    hampathBF = list(findHamiltonianPathBF(graph, len(kmers)))
    BFend = time.time()

    BBstart = time.time()
    hampathBB = findHamiltonianPathBB(graph, len(kmers))
    BBend = time.time()

    if ((len(hampathBF) > 0) and (len(hampathBB) > 0)):
        print("\n ==> (Brute Force) The resulting Hamiltonian Path is:", hampathBF)
        print("\n =====> elapsed time: ", float(BFend - BFstart), " seconds")
        print("\n ==> (Branch & Bound) The resulting Hamiltonian Path is:", hampathBB)
        print("\n =====> elapsed time: ", float(BBend - BBstart), " seconds")

        DNAseq = ""
        for i in hampathBB:
            if len(DNAseq) == 0:
                DNAseq += kmers[i]
            else:
                DNAseq += kmers[i][-1]
        print("\n ==> The reconstructed DNA fragment is: ", DNAseq , "\n")

    else:
        print("\n No Hamiltonian Path found. Cannot reconstruct fragment. \n")


main()
