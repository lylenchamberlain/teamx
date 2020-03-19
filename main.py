from Classes.World import World

import networkx as nx
import plotly.graph_objects as go


#Change for Shrivats
#Change on Computer
myWorld = World()

edgeText = open('SF_edges.txt','r')

'''
edge_x = []
edge_y = []
for edge in edgeText.edges():
    x0, y0 = G.nodes[edge[0]]['pos']
    x1, y1 = G.nodes[edge[1]]['pos']
    edge_x.append(x0)
    edge_x.append(x1)
    edge_x.append(None)
    edge_y.append(y0)
    edge_y.append(y1)
    edge_y.append(None)
'''



print(myWorld.Verticies)

print(myWorld.Edges)

myWorld.runSimulation(10)




