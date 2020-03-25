import numpy as np


class Graph:

  def __init__(self):
    self.neighbors = {} # key - node, value - list of neighbours 
    self.cost = {}  # key - edge, value - cost

  def add_edge(self,u,v,c): #this will add edge (u,v) with cost "c" to the graph
    #print("u ", u, "v ", v, "c ", c )
    if u not in self.neighbors:
      self.neighbors[u]=[]
    if v not in self.neighbors:
      self.neighbors[v]=[]
    if u > v:
      u, v = v, u
    if (u,v) not in self.cost:
      self.neighbors[u].append(v)
      self.neighbors[v].append(u)
      self.cost[(u,v)] = c
      
  def shortest_path2(self, start_node, end_node):
        print("Start_Node", start_node)
        print("MY end_node", end_node)
       
        # let's implement the shortest path algorithm
        d = {} # this will store the "distances from start_node"
        for v in self.neighbors:
          d[v] = np.Inf
        d[start_node] = 0
        
        smallest_node =  start_node 
        permanent = {}
        pre={}
        while smallest_node!= end_node: #Question #1: How many times this can happen? 
          smallest_value = np.Inf 
          smallest_node = None 
          for v in d: # we are searching for the smallest "label" which is not permanent
            if v not in permanent and (d[v] < smallest_value):
              smallest_value = d[v]
              smallest_node = v
          permanent[smallest_node] = True # I am denoting this node with smallest d[v] value as "final" / permanent
          for nv in self.neighbors[smallest_node]: # checking neighbours of "smallest_node" ....
            if nv not in permanent:  # Question #2: is this check "important"? Would it work if I remove it? 
              proposed_distance = d[smallest_node] + self.get_cost(smallest_node, nv)
              if proposed_distance < d[nv]: # if new path via node smallest_node is better, update "d"
                d[nv] = proposed_distance
                pre[nv] = smallest_node
                
                
                
        return Graph.findPath(start_node, end_node, pre)
       
      
        
  def findPath(fromV, toV, pre):
      path = [toV]
      n = None
      while n != fromV:
        n = pre[toV]
        path.insert(0,n)
        toV = n
      return path


    
  def get_cost(self, u,v):
        if u > v:
            u, v = v, u
        if (u,v) in self.cost:
           return self.cost[(u,v)]
        return None
        

