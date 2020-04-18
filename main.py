from Classes.World import World
from Graph import Graph
import random
import networkx as nx   
from Classes.Animation import Animation
import plotly.graph_objects as go
from idlelib import testing
from test.support import resource

#from Graph import shortestPath



myWorld = World()

edgeText = open('SF_edges.txt','r')


#We might not need any of this due to the pickle file
#Array of edge instances, allows us to access edges easier
edgeGraph = Graph()

#Adds edges
for x in range(len(myWorld.Edges)):
    Graph.add_edge(edgeGraph, myWorld.Edges[x][0], myWorld.Edges[x][1], myWorld.Edges[x][2], myWorld.Edges)
    
print("myWorld.edges", myWorld.Edges[0])

print("myWorld.verticies",myWorld.Verticies)


myWorld.runSimulation(10)


#Truck capacity
#Warehouse/processing lines
#Lengths for the edges
#Fix animation

#have an array that ("A", "B", "C")
#get to warehouse A, we just pick up the total A that we need
#Is the truck full
#Whats the fastest way
#Do we have the materials for the processing line

'''
Make a dictionary that stores resource needed for each processing line and how much
For each truck, store an array of how much of eat material hes carrying
[0,0,2,2,0,0]
Make an array of node locations for all warehouses and processing lines
Find the closest anything to where we are now
If its a processing line, check that the truck has the required materials, if not. Go to next closest

    
 Do this loop until there are no more unvisited locations 
   
    for every unvisited location that we have to go to (warehouses and proccesslines)
        get the route from current location to whatever location we are testing
        
    #Returns the shortest path left
    if it is a processline
        check if we have the resource
        unload the resource needed from the truck
        check location as visited
        
    if it is a warehouse
        check we have the truck capactity
        if we do, add the required amount of resource to the truck, and the find the next shortest path
        check location as visited 
    
    find the next shortest path and mark the node as visited


'''







