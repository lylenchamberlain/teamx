from Classes.World import World

import networkx as nx
import plotly.graph_objects as go

<<<<<<< HEAD
###check test
###We probably do not need this class.
=======
#About 8:43 pm

>>>>>>> branch 'master' of https://github.com/lylenchamberlain/teamx.git
class edgeClass():
    
    def  __init__(self, tempArray):
        self.x = tempArray[0]
        self.y = tempArray[1]
        self.z = tempArray[2]
        





myWorld = World()

edgeText = open('SF_edges.txt','r')


#We might not need any of this due to the pickle file
#Array of edge instances


print(myWorld.Verticies)

print(myWorld.Edges)

myWorld.runSimulation(10)

