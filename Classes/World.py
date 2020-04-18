from  Classes.AbstractWorld import AbstractWorld
from Classes.Animation import Animation

import pygame
import random
from Graph import Graph
from array import array
from Tools.demo.sortvisu import quicksort
pygame.font.init() 
#from Animation import Animation

class World(AbstractWorld):
	
	
	def __init__(self):
		AbstractWorld.__init__(self)
		
		self.height = 600
		self.width = 800
		self.screen = pygame.display.set_mode((self.width, self.height))
		self.black = (0,0,0)
		self.clock = pygame.time.Clock()
		self.font  = pygame.font.SysFont('Comic Sans MS', 30)
		self.trucks = self.getInitialTruckLocations()
		#This determines what new order we're on
		self.orderTracker = 0
		self.max = 0
		self.background = pygame.draw.rect(self.screen,(0,0,0),(200,150,100,50))
		#S
		#Create initial animation objects
		self.truckList = []
		self.ProductionLines = []
		self.loopAmount = 0
		self.totalLateTrucks = 0
		self.totalOnTimeTrucks = 0
		self.lateAmounts = []
		
		#Set initial locations and capacities
		for i in self.trucks:
			#Go through all the verticies to determine which one the struck is at
			theCapacity = i.capacity
			for x in self.Verticies:
				#This is the Vertex the truck starts at
				startingNode = i.currentVertex
				#This looks for the vertex identifier in the verticies list and returns x and y value for it
				if x[0] == startingNode:
					startingX = x[1] * 800
					startingY = x[2] * 800
					break
			
			#Create an animation object (it's a truck picture) with the node identifier that it starts at
			myAnimate = Animation(startingNode, theCapacity)
			self.truckList.append(myAnimate)
		self.sortList = []
			
			
		
	def runSimulation(self, fps=1, initialTime=5*60, finalTime=23*60):
		World.assignNodeDuties(self)
		
		#This will give you a list of ALL cars which are in the system
		
		self.trucks = self.getInitialTruckLocations()
		for i,t in enumerate(self.trucks):
			print("vehicle %d: %s"%(i, str(t)))

			
		#Sort the trucks in a list from smalles capacity to biggest
		#Only sort once
		if self.loopAmount != 1:
			World.sortList(self)
			self.loopAmount = 1
				
		for t in range(initialTime,finalTime):	
			print("\n\n Time: %02d:%02d"%(t/60, t%60))

			# each minute we can get a few new orders
			newOrders = self.getNewOrdersForGivenTime(t)
			print("New orders:")
			#Let's graph the truck movements here
			
			
			for c in newOrders:
				print(c)
				print(c.productionProcess)
				print(c.finalLocation)				#I think we should add paths here for specific vehicles
				

			World.drawBackbone(self)
			graphObject = Graph()
			
		
			for c in newOrders:
				

				currentTruck = World.chooseTruck(self, c)
				#Move immediately			
				currentTruck.nextMoveTime =  t
				currentTruck.status = 1
				currentTruck.finalNode = c.finalLocation
				#give it a due date
				currentTruck.dueDate = t + 60				
				
				#Add everything to the truck path
				#Find each warehouse and line
				for x in c.productionProcess:
					matNeeded = x['resourceNeeded']
					#Gives index of the process line we'll use
					processLineNeeded = World.findProcessLine(self,x['processinLine'])
					warehouseNeeded = World.findWarehouse(self, matNeeded)
					#Make them both stops
					currentTruck.stops.append(processLineNeeded)
					#print("PROSO", processLineNeeded)
					currentTruck.stops.append(warehouseNeeded)

					#now lets associate this vertex location with the material needed and the amount
					currentTruck.typeNeeded[processLineNeeded] = matNeeded
					currentTruck.amountNeeded[processLineNeeded] = x['materialNeeded[tons]']
					currentTruck.totalNeeded[warehouseNeeded] = x['materialNeeded[tons]']
					currentTruck.warehouseType[warehouseNeeded] = matNeeded
					currentTruck.timeNeeded[processLineNeeded] = x['processingTime']
					
				#Now we have all the stops it will need to do and matneeded, so we will now create a path
				World.createPath(self, currentTruck, graphObject)
			#Can probably make this a function	
			for truck in self.truckList:
				
				if (truck.status != 4):
					if (t == truck.nextMoveTime):
						truck.smallCounter = truck.smallCounter + 1
						truck.currentNode = truck.completePath[truck.smallCounter]
						if truck.currentNode in truck.timeNeeded:
							truck.nextMoveTime = t + truck.timeNeeded[truck.currentNode]
						
						else:
							truck.nextMoveTime = t + 1
						
						#Takes a while to travel edge to edge
						#Test
						#truck.nextMoveTime = truck.nextMoveTime + World.edgeTime(self, truck.completePath[truck.smallCounter - 1], truck.completePath[truck.smallCounter])
						nice = World.edgeTime(self, truck.completePath[truck.smallCounter - 1], truck.completePath[truck.smallCounter])
						truck.nextMoveTime = truck.nextMoveTime + nice
						#Incorporate edge lengths:
						#Get the path for the two nodes
					
						#graphObject.shortest_path2(truck.currentNode, truck.completePath[truck.smallCounter - 1], self.Edges) 
						
						
					truckLocation = World.nodeToCoordinate(self,truck.currentNode, self.Verticies)
					truckX = 800 * truckLocation[0]
					truckY = 800 * truckLocation[1]
					#Display the current vertex of the truck
					self.screen.blit(truck.ball, (truckX, truckY))
			
					#Got to end of path
					#print("cur", truck.currentNode, truck.finalNode, truck.completePath)
					if (truck.currentNode == truck.finalNode):
						truck.status = 4
						truck.currentPath = []
						truck.completePath = []
						truck.smallCounter = 0
						#Determine if its on time
						if (t <= truck.dueDate):
							self.totalOnTimeTrucks = self.totalOnTimeTrucks + 1
						else:
							self.totalLateTrucks = self.totalLateTrucks + 1
							self.lateAmounts.append(t - truck.dueDate)
						truck.nextMoveTime = 0

			pygame.display.update()	
			self.screen.fill((255,255,255))	
			World.drawScoreboard(self, t)

				#This allows us to exit the game if we want
			if World.quitGame(self, fps) == True:

				break				
			
		print("profit", World.calculateProfit(self))	
		print("LATE", self.totalLateTrucks)
		print("ONTIME", self.totalOnTimeTrucks)	
		print("Late amounts", self.lateAmounts)
		
	#Give it a vertex ID (its unique identifier) this will return the x and y value in a tuple
	def nodeToCoordinate(self, node, worldVerticies):
		for x in worldVerticies:
			if x[0] == node:
				return (x[1],x[2])
			
	def edgeTime(self, node1, node2):

		answer =  2000
		if node1 == node2:
			return 0
		for mine in self.Edges:
			print("GOT HERE", mine[0], node1, mine[1], node2)
			'''for any in self.truckList:
				if any.status != 4:
					print("TOTAL trucks")
			'''
			if (mine[0] == node1) and (mine[1] == node2):
				print("FOUND IT", mine[2])
				answer = mine[2]
				return mine[2]
			
		return World.edgeTime2(self, node2, node1)
		
		
	def edgeTime2(self, node1, node2):
		
		for my in self.Edges:
			if(my[0] == node1) and (my[1] == node2):
				return	my[2]
		
			
	
	
	def calculateProfit(self):
		profit = 0
		profit = (self.totalOnTimeTrucks + self.totalLateTrucks) * 1.5
		penalty = 0
		for ex in  self.lateAmounts:
			calc = ex
			calc = calc / 30
			calc= int(calc)
			calc = calc + 1
			penalty = penalty + calc
		profit = profit - (penalty * .1)
		return profit
		
		
	def sortList(self):
		#We care about truck.capacity
		# Traverse through all array elements 
		for i in range(len(self.truckList)): 
		      
		    # Find the minimum element in remaining  
		    # unsorted array 
		    min_idx = i 
		    for j in range(i+1, len(self.truckList)): 
		        if self.truckList[min_idx].capacity > self.truckList[j].capacity: 
		            min_idx = j 
		              
		    # Swap the found minimum element with  
		    # the first element         
		    self.truckList[i], self.truckList[min_idx] = self.truckList[min_idx], self.truckList[i] 
		return
		

		
	def quitGame(self, fps):
		gameExit = False			
		for event in pygame.event.get():
				
			if event.type == pygame.QUIT:
				gameExit = True
				pygame.quit()
				
		self.clock.tick(fps)
		if gameExit == True:
			return True
		return False
		

	#PRINT EDGES, verticies and timer
	def printMap(self, t):
		for item in range(len(self.Verticies)):
			pygame.draw.rect(self.screen,(0,0,0),(800*self.Verticies[item][1],800*self.Verticies[item][2],10,10))
				
		#Draws Edges onto the screen
		for x in range(len(self.Edges)):
			#Iterate through all the points of path
				for y in range(len(self.Edges[x][3]) - 1):
						pygame.draw.line(self.screen,(90,200,90), (self.Edges[x][3][y][0]*800, self.Edges[x][3][y][1]*800), (self.Edges[x][3][y+1][0]*800, self.Edges[x][3][y+1][1]*800) , 4)
				
		text = self.font.render("Time: %02d:%02d"%(t/60, t%60), True, (255, 0, 0), (255, 255, 255))
		textrect = text.get_rect()
		textrect.centerx = 100
		textrect.centery = 30
		self.screen.blit(text, textrect)
			
	#Returns a value for random vertex. It will only return the integer unique identifying value
	def getRandomVertex(self):
		#Choose a random Vertex from the Verticies
		randomVertex = random.choice(self.Verticies)
		randomVertexValue = randomVertex[0]
		return randomVertexValue 
	
	def assignNodeDuties(self):
		types = ["A","B","C","D","E","F","G","H"]
		ProductionLines = []
		j = 0
		for t in types:
			for k in range(2):
				ProductionLines.append(t)
				j+=1
		
		
		types = ["L1","L2","L3","L4"]
		j = 20
		for t in types:
			for k in range(5):
				ProductionLines.append(t)
				
				j = j + 1
		self.ProductionLines = ProductionLines
		return ProductionLines
	
	def edgeToList(self, startNode, endNode):
		
		#print("Start and end node ", startNode, endNode)
		for x in self.Edges:
			if (x[0] == startNode and x[1] == endNode) or (x[1] == startNode and x[0] == endNode):
				return x[3]
			
		print("ERROR")
		
	def findProcessLine(self, type):
		#Find the node of the process Line
		lineArray = []
		'''Changed the 50 into a 35'''
		for x in range(17, 35):
			if (type ==  self.ProductionLines[x]):
				return self.vShuffled[x]
	
	def findWarehouse(self, resource):
		warehouseOption = []
		'''for y in range(0,16):
			if(resource == self.ProductionLines[y]):
				warehouseOption.append(self.vShuffled[y])
				return self.vShuffled[y]'''
		for y in range(0,16):
			if(resource == self.ProductionLines[y]):
				return self.vShuffled[y]
				
	

	def findLoadSum(self, aTruck):
		total =  0
		for x in aTruck.loadDict:
			total = total + aTruck.loadDict[x]
		return total
				
	def assignMoveTime(self, aTruck):
		pass
	
	def drawScoreboard(self, t):
		text = self.font.render("Time: %02d:%02d"%(t/60, t%60), True, (255, 0, 0), (255, 255, 255))
		textrect = text.get_rect()
		textrect.centerx = 100
		textrect.centery = 30
		#self.screen.fill((255, 255, 255))
		self.screen.blit(text, textrect)
		return
	
	def drawBackbone(self):
	
		#Draw Vertices onto the screen
		for item in range(len(self.Verticies)):
			pygame.draw.rect(self.screen,(0,0,0),(800*self.Verticies[item][1],800*self.Verticies[item][2],10,10))

		#Draws Edges onto the screen
		for x in range(len(self.Edges)):
			#Iterate through all the points of path
			for y in range(len(self.Edges[x][3]) - 1):
				pygame.draw.line(self.screen,(90,200,90), (self.Edges[x][3][y][0]*800, self.Edges[x][3][y][1]*800), (self.Edges[x][3][y+1][0]*800, self.Edges[x][3][y+1][1]*800) , 4)
			
	def chooseTruck(self, c):			
		#Figure out the total capacity that is needed
		totalNeeded = 0
		for theLine in c.productionProcess:
			totalNeeded = totalNeeded + theLine['materialNeeded[tons]'] 
		#Now that we know total needed grab a truck
		currentTruck = 999
		for aTruck in self.truckList:
			if (aTruck.capacity >= totalNeeded and aTruck.status == 4):
				currentTruck = aTruck
				currentTruck.status = 1
				return currentTruck
			
		if currentTruck == 999:		
			for x in range(0, (len(self.truckList)- 1)):
				x  = len(self.truckList) - 1 - x
				if self.truckList[x] != 4:
					currentTruck = self.truckList[x]
					currentTruck.status = 1
					return currentTruck
				
			
			
	def findLength(self, startNode, endNode):
		for edgey in self.Edges:
			if (edgey[0] == startNode) and (edgey[1] == endNode):
				#print("EDGEY", startNode, endNode, edgey[0], edgey[1])
				return edgey[2]
	
	def createPath(self, aTruck, graphObject):
		
		testVertex = aTruck.currentNode
		shortestLength = 100000
		pathToJudge = [1,1,1,1,1,1,1,1,1,1,1,1,1,12,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,23,3]
		#aTruck.currentPath.append(aTruck.currentNode)
		nextNode = 0
		
		
		while len(aTruck.stops) > 0:
			pathToJudge = [1,1,1,1,1,1,1,1,1,1,1,1,1,12,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,23,3]

			for x in aTruck.stops:
				#Go through all the stops
				if(testVertex != x):
					quickGraph = graphObject.shortest_path2(testVertex, x, self.Edges)
					#print("statement", quickGraph)
				else:
					quickGraph = []

					#Check if this is the shortest path so far
				if (len(quickGraph) < len(pathToJudge)):

					#We found a shorter path, lets see if its valid before we do anything
					#Check if its a key for type needed
					if x in aTruck.typeNeeded:

						#If it is that means its a processLine and needs to check if the truck has the required warehouse materials
						theTypeNeeded = aTruck.typeNeeded[x]
						
						#See if we have enough
						if aTruck.loadDict[theTypeNeeded] >= aTruck.amountNeeded[x]:
							#If here we have enough and its a valid path
							nextNode = x
							pathToJudge = quickGraph

					
					#else its a warehouse, add material to the load
					#Check Load
					else:
						#check to see if the truck has enough
						#Find how much it has now
						sum = 0
						for xx in aTruck.loadDict:
							sum = sum + aTruck.loadDict[xx]
						#Now that we have the sum, we can use it to check 
						if (aTruck.capacity >=  (aTruck.totalNeeded[x] + sum)):
							#its good
							nextNode = x
							pathToJudge = quickGraph

			#Get our complete info first
			passer = 0
			for v in pathToJudge:
				if passer != 0:
					aTruck.completePath.append(v)
				else:
					passer = 1
			
				
				#Is it a process line
			if nextNode in aTruck.typeNeeded:
				aTruck.currentPath.append(nextNode)
				#Now we're at the test vertex
				testVertex = nextNode
				#Decrease the values in the truck
				theTypeNeeded = aTruck.typeNeeded[nextNode]

				pastLoad = aTruck.loadDict[theTypeNeeded]
				nowLoad = pastLoad - aTruck.amountNeeded[nextNode]
				aTruck.loadDict[theTypeNeeded] = nowLoad
				#aTruck.currentPath.append(nextNode)
			#else its a warehouse
			else:
				#We can pick up the resources now
				resourceType = aTruck.warehouseType[nextNode]
				#Add the resources to the trucks load
				aTruck.loadDict[resourceType] = aTruck.loadDict[resourceType] + aTruck.totalNeeded[nextNode]
				#this is now a confirmed next destination, so add it
				aTruck.currentPath.append(nextNode)
				testVertex = nextNode
			

			aTruck.stops.remove(nextNode)	
		lastPath = graphObject.shortest_path2(nextNode, aTruck.finalNode, self.Edges)
		
		for numey in lastPath:
			 aTruck.completePath.append(numey)
	
				#It is done with the loop, set truck status to 4
		
		