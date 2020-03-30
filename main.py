from Classes.World import World
from Graph import Graph
import random
import networkx as nx
from Classes.Animation import Animation
import plotly.graph_objects as go

#from Graph import shortestPath


myWorld = World()

edgeText = open('SF_edges.txt','r')
#x = (0,2)
#y = (3,4)
#listy = []
#listy.append(x)
#listy.append(y)
#test = (0,1)
#test2 = test * 2
#print(test2)

#We might not need any of this due to the pickle file
#Array of edge instances, allows us to access edges easier
edgeGraph = Graph()

#Adds edges
for x in range(len(myWorld.Edges)):
    Graph.add_edge(edgeGraph, myWorld.Edges[x][0], myWorld.Edges[x][1], myWorld.Edges[x][2], myWorld.Edges)
        
print("myWorld.verticies",myWorld.Verticies)

print("myWorld.edges", myWorld.Edges)

myWorld.runSimulation(10)

