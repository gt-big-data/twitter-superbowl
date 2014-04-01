import sys
import json
import networkx as nx
import matplotlib.pyplot as plt
import random
from math import e

def draw_g(g):
     pos = nx.spring_layout(g)
     top = sorted(nx.closeness_centrality(g).items(), key=lambda x: x[1])
     top = [k for k, v in top]
     top, rest = top[-8:], top[:-8]
     nx.draw_networkx_nodes(g, pos, nodelist=top, node_color="b")
     nx.draw_networkx_nodes(g, pos, nodelist=rest, node_color="r")
     nx.draw_networkx_edges(g, pos)
     nx.draw_networkx_labels(g, pos)

def sample(l, weights):
    weightL = list(zip(l, weights))
    weightL.sort(key=lambda x: -x[1]) # desc
    totalWeight = sum(weights)
    stoppingPoint = random.random() * totalWeight
    weight = 0.
    for i in range(len(weightL)):
        weight += weightL[i][1]
        if weight >= stoppingPoint:
            return weightL[i][0]
    raise ValueError("Could not sample")


def generateTweet(g, top):
    sentence = []
    start = random.choice(top)
    cur = start
    chars = 0
    targetLen = 30 * (random.random() - 0.5) + 120
    prevA, prevB, prevC = None, None, None
    visited = set([])
    res = ""
    while len(res) < targetLen:
        a, b, c = cur
        if prevA and prevA == a and prevB == b and prevC == c: 
            pass
        elif prevB and b == prevB and prevC == a:
            res += " " + c
        elif prevC and prevC == a:
            res += " "  + b + " " + c
        else:
            res += " " if prevA else "" + a + " " + b + " " + c
        prevA, prevB, prevC = a, b, c
        
        visited.add(cur)
        if len(res) > targetLen: break;

        edges = [(b, weight['weight']) for _, b, weight in g.edges(cur, data=True) if b not in visited ]
        if not edges: 
            break;
        nextVertex, _ = sample(edges, weights=[e**-w for _, w in edges ])
        cur = nextVertex
    return res

def nxGraphToD3Graph(g):
    nodes = {i: " ".join(node) for i, node in enumerate(g.nodes())}
    reverse = {node: i for i, node in enumerate(g.nodes())}
    edges = [ ]
    for a, b, data in g.edges(data=True): 
        d3HappyEdge = {
                "source": reverse[a],
                "target": reverse[b],
                "weight" : data['weight']
                }
        edges.append(d3HappyEdge)
    d3HappyEdges = edges
    d3HappyNodes = []
    for i in xrange(len(nodes)):
        if i not in nodes:
            raise ValueError("WTF")
        d3HappyNodes.append(nodes[i])
    return { "nodes" : d3HappyNodes, "links" : d3HappyEdges }

def genGraph(top3grams, trivialWords):
    gramsGraph = nx.Graph()
    allThreegrams = [tuple(g[0]) for g in top3grams['top']] 
    gramsGraph.add_nodes_from(allThreegrams)
    pairs = ((i,j) for i in range(len(allThreegrams)) for j in range(len(allThreegrams)) if i < j)
    for i, j in pairs:
        a = allThreegrams[i]
        b = allThreegrams[j]
        a1, a2, a3 = a
        b1, b2, b3 = b
        overlap = []
        if a1 == b3 and b2 == a2:
            overlap.append(a1)
            overlap.append(a2)
        elif b1 == a3 and b2 == a2:
            overlap.append(b1)
            overlap.append(b2)
        elif a1 == b3:
            overlap.append(a1)
        elif b1 == a3:
            overlap.append(b1)

        if len(overlap) == 1:
            if overlap[0] in trivialWords:
                gramsGraph.add_edge(a, b, weight=20)
            else:
                gramsGraph.add_edge(a, b, weight=4)
        elif len(overlap) == 2:
            if all(g in trivialWords for g in overlap):
                gramsGraph.add_edge(a, b, weight=8)
            elif overlap[0] in trivialWords and overlap[1] not in trivialWords:
                gramsGraph.add_edge(a, b, weight=2)
            elif overlap[1] in trivialWords and overlap[0] not in trivialWords:
                gramsGraph.add_edge(a, b, weight=3)
            else:
                gramsGraph.add_edge(a, b, weight=1)
    return gramsGraph

def main():
    trivialWords = set([ 'the', 'a', 'i', 'am', 'rt' ])
    periods = {}
    higherOrder = {}
    with open("./top-ngrams.json", 'r') as f:
        for line in f:
            top3grams = json.loads(line)
            period = int(top3grams['per'])
            periods[period]= genGraph(top3grams, trivialWords)

    with open("out.json", "w") as f:
        prev = None
        for period, g in periods.items(): 
            print "writing ", period 
            top = sorted(nx.closeness_centrality(g).items(), key=lambda x: x[1])
            top = top[:-8]
            top = [k for k, v in top]
            randTweets = [generateTweet(g, top) for _ in xrange(10)]
            #g = nxGraphToD3Graph(g)
            g = {}
            g['tweets'] = randTweets
            g['per'] = period
            if not prev:
                print >>f, "[" 
            else:
                print >>f, prev + ","
            prev = json.dumps(g) 
        print >>f, prev, "]"


if __name__ == '__main__':
    main()
