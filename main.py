from Classes.World import World
from Graph import Graph
import random
import networkx as nx
import plotly.graph_objects as go
#from Graph import shortestPath


myWorld = World()

edgeText = open('SF_edges.txt','r')


#We might not need any of this due to the pickle file
#Array of edge instances
edgeGraph = Graph()

#Adds edges
for x in range(len(myWorld.Edges)):
    Graph.add_edge(edgeGraph, myWorld.Edges[x][0], myWorld.Edges[x][1], myWorld.Edges[x][2])
    
    
#Random test for shortest path
testValue1 = 1
testValue2 = 1

while testValue1 == testValue2:
    testValue1 = random.choice(myWorld.Verticies)
    testValue2 = random.choice(myWorld.Verticies)

firstNode = testValue1[0]
secondNode = testValue2[0]
#This is just for consistency
firstNode = myWorld.Verticies[0][0]
secondNode = myWorld.Verticies[1][0]

Graph.shortest_path(edgeGraph,firstNode,secondNode)



print(myWorld.Verticies)

print(myWorld.Edges)

myWorld.runSimulation(10)

