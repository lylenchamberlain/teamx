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



#firstNode = testValue1[0]
#secondNode = testValue2[0]
#print("Carolines first node", testValue1)
#print("Caroline confirm", testValue1)

#This is Wrong but it runs

#firstNode = myWorld.Verticies[]
#secondNode = myWorld.Verticies[random2]

#print("TestValue1 ", testValue1)

#print("FIRST NODE = ", firstNode)
#print("SECOND NODE = ", secondNode)

#testValue 1 is an array with three values of the vertex
#The first one is a unique value identifying the node, the next two are x and y coordinates.
nodeIdentifier1 = testValue1[0]
nodeIdentifier2 = testValue2[0]
Graph.shortest_path2(edgeGraph,nodeIdentifier1,  nodeIdentifier2)



print("myWorld.verticies",myWorld.Verticies)

print("myWorld.edges", myWorld.Edges)

myWorld.runSimulation(10)

