import sys
import json
import networkx as nx
import matplotlib.pyplot as plt

def draw_g(g):
     pos = nx.spring_layout(g)
     top = sorted(nx.closeness_centrality(g).items(), key=lambda x: x[1])
     top = [k for k, v in top]
     top, rest = top[-8:], top[:-8]
     nx.draw_networkx_nodes(g, pos, nodelist=top, node_color="b")
     nx.draw_networkx_nodes(g, pos, nodelist=rest, node_color="r")
     nx.draw_networkx_edges(g, pos)
     nx.draw_networkx_labels(g, pos)

def main():
    trivialWords = {'the', 'a', 'i', 'am', 'rt'}
    periods = {}
    higherOrder = {}
    for line in sys.stdin:
        top3grams = json.loads(line)
        period = int(top3grams['per'])
        periods[period]= top3grams['top']
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
                    

        # byDegrees = sorted(nx.degree(gramsGraph).items(), key=lambda x: x[1])
        # m = byDegrees[-1]
        # include = [(k, v) for k, v in byDegrees if v > 3. / 4. * m[1]]
        include = gramsGraph
        periods[period] = include

    import IPython;IPython.embed_kernel();



if __name__ == '__main__':
    main()
