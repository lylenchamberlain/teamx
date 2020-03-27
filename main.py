from Classes.World import World
from Graph import Graph
import random
import networkx as nx
from Classes.Animation import Animation
import plotly.graph_objects as go
#from Graph import shortestPath


myWorld = World()

edgeText = open('SF_edges.txt','r')


#We might not need any of this due to the pickle file
#Array of edge instances
edgeGraph = Graph()
#mainAnimationObject = Animation()


#Adds edges
for x in range(len(myWorld.Edges)):
    Graph.add_edge(edgeGraph, myWorld.Edges[x][0], myWorld.Edges[x][1], myWorld.Edges[x][2])
    

#print("VALUE", mainAnimationObject.value)
    
#Random test for shortest path
testValue1 = 1
testValue2 = 1

while testValue1 == testValue2:
    testValue1 = random.choice(myWorld.Verticies)
    testValue2 = random.choice(myWorld.Verticies)





#testValue 1 is an array with three values of the vertex
#The first one is a unique value identifying the node, the next two are x and y coordinates.
nodeIdentifier1 = testValue1[0]
nodeIdentifier2 = testValue2[0]
ourShortestPath = Graph.shortest_path2(edgeGraph,nodeIdentifier1,  nodeIdentifier2)



#myAnimate = Animation()
#    print("Animate it ", myAnimate.value)

print("myWorld.verticies",myWorld.Verticies)

print("myWorld.edges", myWorld.Edges)
#myWorld.generateTruckList()
myWorld.runSimulation(10)

