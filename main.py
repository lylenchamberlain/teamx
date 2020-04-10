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
#Array of edge instances, allows us to access edges easier
edgeGraph = Graph()

#Adds edges
for x in range(len(myWorld.Edges)):
    Graph.add_edge(edgeGraph, myWorld.Edges[x][0], myWorld.Edges[x][1], myWorld.Edges[x][2], myWorld.Edges)
        
print("myWorld.verticies",myWorld.Verticies)

print("myWorld.edges", myWorld.Edges)

myWorld.runSimulation(10)

