from Classes.World import World

import networkx as nx
import plotly.graph_objects as go


###We probably do not need this class.
class edgeClass():
    
    def  __init__(self, tempArray):
        self.x = tempArray[0]
        self.y = tempArray[1]
        self.z = tempArray[2]
        





myWorld = World()

edgeText = open('SF_edges.txt','r')


#We might not need any of this due to the pickle file
#Array of edge instances
edgeArray = []
for line in edgeText:
    
    #Split elements of edges into arrays
    tempArray = (line.split(","))
    tempArray[-1] = int(tempArray[-1].strip())
    tempArray[0] = int(tempArray[0])
    tempArray[1] = int(tempArray[1])
    newAddition = edgeClass(tempArray)
    edgeArray.append(newAddition)
    print(tempArray)


print(myWorld.Verticies)

print(myWorld.Edges)

myWorld.runSimulation(10)

