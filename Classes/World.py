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
		self.transportationCost = 0
		
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

		#Assigns whether vertices are process lines or warehouses
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
				
			#Draw the edges and vertexes
			World.drawBackbone(self)
			graphObject = Graph()
			
			for c in newOrders:
				
				skip = 0
				#Choose which truck to use
				currentTruck = World.chooseTruck(self, c)
				#If no trucks available
				#Reset truck to factory deault
				World.completeTruckReset(self, currentTruck, currentTruck.currentNode, currentTruck.capacity)

				#Move immediately			
				currentTruck.nextMoveTime =  t
				currentTruck.status = 1
				currentTruck.finalNode = c.finalLocation
				#give it a due date
				currentTruck.dueDate = t + 60				
				
				#
				World.assignVertexFacts2(self, c, currentTruck)	
				#Okay now we assign what each vertex requires
				#Now we have all the stops it will need to do and matneeded, so we will now create a path
				''''''
				World.createPath2(self, currentTruck, graphObject, newOrders)
			#Can probably make this a function	
			
			for truck in self.truckList:
				
				
				if (truck.status != 4):
					if (t == truck.nextMoveTime):
						
						truck.smallCounter = truck.smallCounter + 1
						#Increase and then assign current node
						truck.currentNode = truck.completePath[truck.smallCounter]
						#Check if the small counter has a time
						if (truck.smallCounter in truck.smallIndexTime) and (truck.currentNode in truck.timeNeeded):
							truck.nextMoveTime = t + truck.timeNeeded[truck.currentNode]

						
						else:
							truck.nextMoveTime = t
						
						#Takes a while to travel edge to edge
						#Test
						#truck.nextMoveTime = truck.nextMoveTime + World.edgeTime(self, truck.completePath[truck.smallCounter - 1], truck.completePath[truck.smallCounter])
						#print("Trook", truck.completePath[truck.smallCounter - 1], truck.completePath[truck.smallCounter])
						nice = World.edgeTime(self, truck.completePath[truck.smallCounter - 1], truck.completePath[truck.smallCounter], 1)
						indexToCheck = truck.smallCounter - 1
						self.transportationCost = self.transportationCost + (((50 + (5 * nice * truck.currentLoadSum[indexToCheck])))* .00001)
						'''
						#so nice + the load at the previous node
						
						'''
						truck.nextMoveTime = truck.nextMoveTime + nice
						
					truckLocation = World.nodeToCoordinate(self,truck.currentNode, self.Verticies)
					truckX = 800 * truckLocation[0]
					truckY = 800 * truckLocation[1]
					#Display the current vertex of the truck
					self.screen.blit(truck.ball, (truckX, truckY))
				
				#Got to end of path
				#print("cur", truck.currentNode, truck.finalNode, truck.completePath)
				if (truck.smallCounter == (len(truck.completePath) - 2)):
					World.truckIsDone(self, truck, t)

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
		print("transportation Costs", self.transportationCost)
		
	#Give it a vertex ID (its unique identifier) this will return the x and y value in a tuple
	def nodeToCoordinate(self, node, worldVerticies):
		for x in worldVerticies:
			if x[0] == node:
				return (x[1],x[2])
			
	def truckIsDone(self, truck, t):
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
		return 
	
	def edgeTime(self, node1, node2, loopCount):
		
		answer =  2000
		
		if loopCount == 3:
			print("yeehaw")
			return
		if node1 == node2:
			return 0
		for mine in self.Edges:
			'''for any in self.truckList:
				if any.status != 4:
					print("TOTAL trucks")
			'''
			if ((mine[0] == node1) and (mine[1] == node2)) or ((mine[0] == node2) and (mine[1] == node1)):
				answer = mine[2]
				return mine[2]
		print("error")
		loopCount = loopCount + 1
		return 800
		
		
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
		profit = profit - self.transportationCost
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
		#Add types to an array called production range
		types = ["A","B","C","D","E","F","G","H"]
		ProductionLines = []
		j = 0
		for t in types:
			#Add two warehouses of each type
			for k in range(2):
				ProductionLines.append(t)
				j+=1
		
		
		types = ["L1","L2","L3","L4"]
		j = 20
		for t in types:
			#Gives 5 of each line type and appends it
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
		
	
	
	def findProcessArray(self, type):
		processArray = []
		for x in range(16, 35):
			if (type == self.ProductionLines[x]):
				processArray.append(self.vShuffled[x])
		return processArray				
		
		
	def findWarehouseArray(self, resource):
		warehouseArray = []
		for y in range(0,15):
			if(resource == self.ProductionLines[y]):
				warehouseArray.append(self.vShuffled[y])
		return warehouseArray
	

	def findLoadSum(self, aTruck):
		total =  0
		for x in aTruck.loadDict:
			total = total + aTruck.loadDict[x]
		return total
				
	def assignMoveTime(self, aTruck):
		pass
	
	def completeTruckReset(self, currentTruck, currentVertex, capacity):
		currentTruck.currentNode = currentVertex
		

		#This counter is used to figure out what point on the h the truck is at
		currentTruck.smallCounter = 0
		currentTruck.finalNode = 1000
		currentTruck.processTimes = []

		currentTruck.currentLoad = "" #String of the job its carrying
		currentTruck.thirdListEasy = []
		currentTruck.truckPath = []
		currentTruck.timeNeeded = []
		currentTruck.dict = {}
		currentTruck.stops = []
		currentTruck.capacity = capacity
		currentTruck.loadSize = 0
		currentTruck.loadDict = {
			'A' : 0,
			'B' : 0,
			'C' : 0,
			'D' : 0,
			'E' : 0,
			'F' : 0,
			'G' : 0, 
			'H' : 0
			}
		currentTruck.totalNeeded = {}
		currentTruck.typeNeeded = {}
		currentTruck.timeNeeded = {}
		currentTruck.amountNeeded = {}
		currentTruck.warehouseType = {}
		currentTruck.currentPath = []
		currentTruck.nextMoveTime = 0
		currentTruck.dueDate = 0
		currentTruck.completePath = []
		currentTruck.truckX = 0
		currentTruck.truckY = 0
		currentTruck.smallIndexTime.clear()
		currentTruck.currentLoadSum.clear()

	def drawScoreboard(self, t):
		text = self.font.render("Time: %02d:%02d"%(t/60, t%60), True, (255, 0, 0), (255, 255, 255))
		textrect = text.get_rect()
		textrect.centerx = 100
		textrect.centery = 30
		#self.screen.fill((255, 255, 255))
		self.screen.blit(text, textrect)
		return
	
	def assignVertexFacts(self, c, currentTruck):
		
		#For each step in the new order
		for x in c.productionProcess:
			#material needed in the step
			matNeeded = x['resourceNeeded']
			#Gives index of the process line and warehousewe'll use
			processLineNeeded = World.findProcessLine(self, x['processinLine'])
			warehouseNeeded = World.findWarehouse(self, matNeeded)
			#Make them both stops
			
			currentTruck.stops.append(processLineNeeded)
			#print("PROSO", processLineNeeded)
			currentTruck.stops.append(warehouseNeeded)

			#now lets associate this vertex location with the material needed and the amount
			#The following usee the index as the node value of the process line
			#Gives material needed at node
			currentTruck.typeNeeded[processLineNeeded] = matNeeded
			#Gives amount needed at node
			currentTruck.amountNeeded[processLineNeeded] = x['materialNeeded[tons]']
			#Time needed at node value
			currentTruck.timeNeeded[processLineNeeded] = x['processingTime']

			#currentTruck.timeNeeded[processLineNeeded] = 0
			#For warehouse node value
			currentTruck.timeNeeded[warehouseNeeded]= 0
			#Amount of material needed
			currentTruck.totalNeeded[warehouseNeeded] = x['materialNeeded[tons]']
			#Specific material needed
			currentTruck.warehouseType[warehouseNeeded] = matNeeded
			#print("warehouses", warehouseNeeded)
			#print("warehouses", processLineNeeded)
		#print("STOPS", currentTruck.stops)
	
		
	def assignVertexFacts2(self, c, currentTruck):
		
		#For each step in the new order
		for x in c.productionProcess:
			#material needed in the step
			matNeeded = x['resourceNeeded']
			#Gives index of the process line and warehousewe'll use
			processLinesNeeded = World.findProcessArray(self, x['processinLine'])
			warehousesNeeded = World.findWarehouseArray(self, matNeeded)
			#Make them both stops
			currentTruck.stops.append(processLinesNeeded)
			#print("PROSO", processLineNeeded)
			currentTruck.stops.append(warehousesNeeded)
			print("appley", warehousesNeeded, processLinesNeeded)
			
	
			#now lets associate this vertex location with the material needed and the amount
			#The following usee the index as the node value of the process line
			#Gives material needed at node
			for a in warehousesNeeded:
				#currentTruck.timeNeeded[processLineNeeded] = 0
				#For warehouse node value
				currentTruck.timeNeeded[a]= 0
				#Amount of material needed
				currentTruck.totalNeeded[a] = x['materialNeeded[tons]']
				#Specific material needed
				currentTruck.warehouseType[a] = matNeeded
			
			for b in processLinesNeeded:
				currentTruck.typeNeeded[b] = matNeeded
				#Gives amount needed at node
				currentTruck.amountNeeded[b] = x['materialNeeded[tons]']
				#Time needed at node value
				currentTruck.timeNeeded[b] = x['processingTime']
		
	
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
		
		if currentTruck == 999:
			while true:
				pass
			return 1010
		
				
	def findLength(self, startNode, endNode):
		for edgey in self.Edges:
			if (edgey[0] == startNode) and (edgey[1] == endNode):
				#print("EDGEY", startNode, endNode, edgey[0], edgey[1])
				return edgey[2]
		
	def transportCost(self, aTruck):
		#determine how much total
		#when we get to a stop (process line or warehouse) check again
		pass
	
	def truckLoad(self, aTruck):
		sum = 0
		for xx in aTruck.loadDict:
			sum = sum + aTruck.loadDict[xx]
		return sum
		
	def createPath(self, aTruck, graphObject, newOrders):
		'''
		profit 214.1005999999997
		LATE 237
		ONTIME 1
		Late amounts [23, 52, 97, 48, 74, 110, 106, 37, 123, 98, 51, 136, 103, 158, 136, 139, 101, 99, 140, 142, 124, 141, 152, 182, 126, 195, 119, 123, 148, 131, 96, 168, 97, 157, 105, 179, 163, 172, 33, 110, 126, 127, 149, 106, 145, 75, 114, 215, 123, 216, 193, 160, 205, 76, 198, 173, 198, 107, 68, 127, 199, 75, 117, 217, 169, 151, 157, 76, 72, 48, 86, 153, 178, 101, 118, 205, 125, 188, 123, 154, 203, 178, 195, 176, 142, 154, 160, 158, 127, 160, 145, 77, 189, 169, 164, 129, 203, 179, 194, 126, 175, 153, 191, 126, 189, 189, 145, 142, 177, 215, 149, 158, 133, 158, 196, 157, 178, 89, 139, 145, 109, 150, 207, 133, 120, 181, 126, 81, 158, 89, 97, 69, 156, 112, 118, 143, 120, 114, 142, 118, 249, 97, 153, 148, 123, 56, 206, 130, 174, 146, 188, 171, 112, 111, 169, 179, 132, 168, 53, 172, 75, 122, 150, 120, 102, 139, 161, 185, 133, 185, 64, 66, 83, 246, 171, 194, 105, 121, 125, 126, 125, 104, 46, 176, 85, 92, 145, 51, 164, 140, 138, 162, 103, 123, 155, 188, 162, 131, 114, 87, 133, 135, 129, 122, 174, 194, 86, 162, 66, 143, 206, 51, 104, 114, 203, 139, 163, 184, 152, 162, 149, 169, 104, 160, 138, 106, 133, 184, 177, 123, 161, 174, 952, 162, 61, 100, 99]
		transportation Costs 19.499400000000303
		'''
	
		#Test vertex is the node that wew branch off to find other ones
		testVertex = aTruck.currentNode
		#These values are to assure that shorter paths are found and we never keep this one
		shortestLength = 100000
		pathToJudge = [1,1,1,1,1,1,1,1,1,1,1,1,1,12,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,23,3,1,1,1,1,1,1,1]
		nextNode = 10000000000
		#The first step of the path should be the trucks current vertex
		aTruck.completePath.append(testVertex)
		
		#While their are still stops, because we remove every stop when we add it to truck path
		while len(aTruck.stops) > 0:
			#Make sure this is the longest path and it will be changed with a smaller option
			pathToJudge = [1,1,1,1,1,1,1,1,1,1,1,1,1,12,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,23,3, 2,2,2,2,2,2,2,2,2]
			#For every stop in the truck's list of stops
			for x in aTruck.stops:
	
				#don't try to make a path from one vertex to the same one because it won't work, instead create a blank path
				if(testVertex != x):
					quickGraph = graphObject.shortest_path2(testVertex, x, self.Edges)
					skip = 0
					#print("statement", quickGraph)
				else:
					#Don't route from the path we're at to the same one, create a graph of length 0, and skip the loop that trys to find a shorter loop
					quickGraph = []
					#Don't bother looking at other paths
					#Set this node as the shortest path
					nextNode = x
					nextNode = testVertex
					#Don't bother finding a shorter path
					skip = 1
	
				#skip is 0 if we haven't found a path of length 0
				if skip == 0:
					
					#quick graph is the path we create from one node to another
					#The path to judge is the current shortest path
					
					#Check if the quick graph is less than the one we're judging
					if (len(quickGraph) < len(pathToJudge)):
						#We found a shorter path, lets see if its valid before we do anything
						#Check if its a key for type needed, only processLines will be in this graph
						if x in aTruck.typeNeeded:
							#If here it is a processLine and needs to check if the truck has the required warehouse materials
							#first what type of resource does it need?
							theTypeNeeded = aTruck.typeNeeded[x]
							
							#See if we have enough in the truck
							if aTruck.loadDict[theTypeNeeded] >= aTruck.amountNeeded[x]:
								#If here we have enough and its a valid path
								nextNode = x
								pathToJudge = quickGraph
							else:
								#If we don't have enough materials for the the process line we can't add this to our path yet
								continue
	
						#If on our stop list and not a processs line, its a warehouse
						#Check Load
						else:
							#check to see if the truck has enough capacity
							#Find how much it has now
	
							sum = World.truckLoad(self, aTruck)
							#Now that we have the sum, we can use it to check 
							if (aTruck.capacity >=  (aTruck.totalNeeded[x] + sum)):
								#it has enough capacity to pick up the capacity needed
								#this is a valid path length to check
								nextNode = x
								pathToJudge = quickGraph
	
			#end of for loop, so by now we have found the shortest valid path to the vertex we're testing (testVertex)
			#Append the list but don't use the first value, use passer so we don't add the first element twice
			passer = 0
			#We're gonna have to add transporting costs
			transportingCost = World.transportCost(self, aTruck)
			
			sum = World.truckLoad(self, aTruck)
			aTruck.currentLoadSum[0] = 0
			for v in pathToJudge:
				#This if  statement skips the append of the first element in pathToJude
				if passer != 0:
					aTruck.completePath.append(v)
					#We also record the trucks currentLoad at this point (it won't change)
					indexer = len(aTruck.completePath) - 1 #This is the index at the new point
					aTruck.currentLoadSum[indexer] = sum
				else:
					passer = 1
				
				
			#how do we just do the new stuff?
			
			#Make sure the graph has elements or else we skipped the order
			#The complete path is appended every time we have a warehouse or process lines
			
			if (len(aTruck.completePath)!= 0):
				#At the end  of each path portion we have an activity that needs to  be done. We add a arbitrary value of 1 for now
				#The more important part of this is that it saves the index in the path where an action is needed.
				doSomethingHere = len(aTruck.completePath) - 1
				aTruck.timeNeeded[doSomethingHere] = 1
				#We also need to say the capacity may change here
				'''
				currentLoad = World.truckLoad(self, aTruck)
				aTruck.currentLoadSum[doSomethingHere] = currentLoad
				'''
				
			#This will mean its a processLine if it has a typeNeeded
			if nextNode in aTruck.typeNeeded:
	
				#Now we're at the test vertex
				#Decrease the values in the truck
				theTypeNeeded = aTruck.typeNeeded[nextNode]
				pastLoad = aTruck.loadDict[theTypeNeeded]
				nowLoad = pastLoad - aTruck.amountNeeded[nextNode]
				aTruck.loadDict[theTypeNeeded] = nowLoad
	
				
			#If not a processLine its a warehouse
			else:
				#We can pick up the resources now
				resourceType = aTruck.warehouseType[nextNode]
				#Add the resources to the trucks load
				aTruck.loadDict[resourceType] = aTruck.loadDict[resourceType] + aTruck.totalNeeded[nextNode]
	
			
			#Once we add the truck to the path and take the necessary action, remove it so it can't be used again 			
			aTruck.stops.remove(nextNode)
			testVertex =  nextNode
			
	
		#At the very end add a path into the job order destination
		lastPath = graphObject.shortest_path2(nextNode, aTruck.finalNode, self.Edges)
		
		
		sumNow = World.truckLoad(self, aTruck)
		#This just makes sure we add the last path to the complete truck path, and we don't double add the last elemeent
		start = 0
		for numey in lastPath:
			if start == 1:
			 	aTruck.completePath.append(numey)
			 	aTruck.currentLoadSum[len(aTruck.completePath) - 1] = sumNow
			else:
				start = 1
	
	
	def createTrainPath(self, aTruck, graphObject, newOrders):
			
			
			#Test vertex is the node that wew branch off to find other ones
			testVertex = aTruck.currentNode
			#These values are to assure that shorter paths are found and we never keep this one
			shortestLength = 100000
			pathToJudge = [1,1,1,1,1,1,1,1,1,1,1,1,1,12,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,23,3,1,1,1,1,1,1,1]
			nextNode = 10000000000
			#The first step of the path should be the trucks current vertex
			aTruck.completePath.append(testVertex)
			
			#While their are still stops, because we remove every stop when we add it to truck path
			while len(aTruck.stops) > 0:
				#Make sure this is the longest path and it will be changed with a smaller option
				pathToJudge = [1,1,1,1,1,1,1,1,1,1,1,1,1,12,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,23,3, 2,2,2,2,2,2,2,2,2]
				#For every stop in the truck's list of stops
				for x in aTruck.stops:
	
					#don't try to make a path from one vertex to the same one because it won't work, instead create a blank path
	
						#print("statement", quickGraph)
					if (testVertex == x):
						#Don't route from the path we're at to the same one, create a graph of length 0, and skip the loop that trys to find a shorter loop
						quickGraph = []
						#Don't bother looking at other paths
						#Set this node as the shortest path
						nextNode = x
						nextNode = testVertex
						#Don't bother finding a shorter path
						skip == 1
					#skip is 0 if we haven't found a path of length 0
					if skip == 0:
						
						#quick graph is the path we create from one node to another
						#The path to judge is the current shortest path
	
							#We found a shorter path, lets see if its valid before we do anything
							#Check if its a key for type needed, only processLines will be in this graph
							if x in aTruck.typeNeeded:
								#If here it is a processLine and needs to check if the truck has the required warehouse materials
								#first what type of resource does it need?
								theTypeNeeded = aTruck.typeNeeded[x]
								
								#See if we have enough in the truck
								if aTruck.loadDict[theTypeNeeded] >= aTruck.amountNeeded[x]:
									#If here we have enough and its a valid path
									nextNode = x
									pathToJudge = quickGraph
								else:
									#If we don't have enough materials for the the process line we can't add this to our path yet
									continue
	
							#If on our stop list and not a processs line, its a warehouse
							#Check Load
							else:
								#check to see if the truck has enough capacity
								#Find how much it has now
	
								sum = World.truckLoad(self, aTruck)
								#Now that we have the sum, we can use it to check 
								if (aTruck.capacity >=  (aTruck.totalNeeded[x] + sum)):
									#it has enough capacity to pick up the capacity needed
									#this is a valid path length to check
									nextNode = x
									pathToJudge = quickGraph
	
				#end of for loop, so by now we have found the shortest valid path to the vertex we're testing (testVertex)
				#Append the list but don't use the first value, use passer so we don't add the first element twice
				passer = 0
				#We're gonna have to add transporting costs
				transportingCost = World.transportCost(self, aTruck)
				
				sum = World.truckLoad(self, aTruck)
				aTruck.currentLoadSum[0] = 0
				for v in pathToJudge:
					#This if  statement skips the append of the first element in pathToJude
					if passer != 0:
						aTruck.completePath.append(v)
						#We also record the trucks currentLoad at this point (it won't change)
						indexer = len(aTruck.completePath) - 1 #This is the index at the new point
						aTruck.currentLoadSum[indexer] = sum
					else:
						passer = 1
					
					
				#how do we just do the new stuff?
				
				#Make sure the graph has elements or else we skipped the order
				#The complete path is appended every time we have a warehouse or process lines
				
				if (len(aTruck.completePath)!= 0):
					#At the end  of each path portion we have an activity that needs to  be done. We add a arbitrary value of 1 for now
					#The more important part of this is that it saves the index in the path where an action is needed.
					doSomethingHere = len(aTruck.completePath) - 1
					aTruck.timeNeeded[doSomethingHere] = 1
					#We also need to say the capacity may change here
					'''
					currentLoad = World.truckLoad(self, aTruck)
					aTruck.currentLoadSum[doSomethingHere] = currentLoad
					'''
					
				#This will mean its a processLine if it has a typeNeeded
				if nextNode in aTruck.typeNeeded:
	
					#Now we're at the test vertex
					#Decrease the values in the truck
					theTypeNeeded = aTruck.typeNeeded[nextNode]
					pastLoad = aTruck.loadDict[theTypeNeeded]
					nowLoad = pastLoad - aTruck.amountNeeded[nextNode]
					aTruck.loadDict[theTypeNeeded] = nowLoad
		
					
				#If not a processLine its a warehouse
				else:
					#We can pick up the resources now
					resourceType = aTruck.warehouseType[nextNode]
					#Add the resources to the trucks load
					aTruck.loadDict[resourceType] = aTruck.loadDict[resourceType] + aTruck.totalNeeded[nextNode]
	
				
				#Once we add the truck to the path and take the necessary action, remove it so it can't be used again 			
				aTruck.stops.remove(nextNode)
				testVertex =  nextNode
				
		
			#At the very end add a path into the job order destination
			lastPath = graphObject.shortest_path2(nextNode, aTruck.finalNode, self.Edges)
			
			
			sumNow = World.truckLoad(self, aTruck)
			#This just makes sure we add the last path to the complete truck path, and we don't double add the last elemeent
			start = 0
			for numey in lastPath:
				if start == 1:
				 	aTruck.completePath.append(numey)
				 	aTruck.currentLoadSum[len(aTruck.completePath) - 1] = sumNow
				else:
					start = 1
		
	def createPath2(self, aTruck, graphObject, newOrders):
		'''
		profit 312.89264999999915
		LATE 296
		ONTIME 1
		Late amounts [18, 55, 62, 49, 68, 92, 21, 105, 95, 60, 90, 119, 52, 91, 42, 53, 84, 46, 146, 113, 100, 89, 106, 55, 147, 86, 75, 166, 87, 127, 103, 50, 63, 116, 149, 163, 151, 74, 147, 123, 33, 129, 92, 72, 163, 164, 92, 174, 110, 116, 51, 142, 74, 173, 43, 176, 140, 28, 126, 168, 57, 142, 57, 70, 37, 181, 83, 131, 50, 154, 95, 122, 95, 78, 90, 113, 80, 105, 76, 30, 109, 76, 63, 87, 73, 113, 37, 47, 144, 173, 79, 134, 140, 121, 118, 88, 78, 88, 159, 142, 87, 123, 109, 124, 101, 118, 127, 124, 159, 188, 183, 115, 139, 130, 58, 138, 59, 92, 91, 146, 164, 96, 118, 90, 93, 129, 74, 96, 107, 158, 158, 119, 65, 119, 54, 71, 38, 111, 39, 117, 150, 99, 128, 83, 120, 68, 111, 116, 180, 26, 66, 80, 77, 95, 121, 90, 122, 104, 47, 125, 110, 88, 83, 41, 138, 94, 97, 97, 124, 19, 73, 84, 108, 112, 151, 103, 24, 12, 90, 39, 76, 146, 125, 167, 166, 91, 146, 117, 93, 29, 137, 121, 6, 129, 101, 83, 115, 88, 73, 128, 19, 98, 151, 48, 99, 38, 35, 115, 159, 90, 123, 146, 129, 53, 186, 50, 66, 100, 145, 71, 108, 192, 103, 106, 112, 175, 137, 119, 45, 138, 20, 78, 95, 106, 169, 94, 102, 61, 171, 116, 126, 98, 82, 73, 72, 57, 151, 129, 79, 68, 185, 92, 63, 55, 55, 121, 53, 107, 145, 181, 76, 64, 105, 143, 87, 79, 138, 146, 88, 67, 52, 128, 146, 100, 161, 135, 158, 166, 126, 163, 6, 128, 42, 165, 79, 42, 72, 139, 74, 59, 80, 98, 115, 157, 22, 50]
		transportation Costs 17.70735000000085
		'''
	
		#Test vertex is the node that wew branch off to find other ones
		testVertex = aTruck.currentNode
		#These values are to assure that shorter paths are found and we never keep this one
		shortestLength = 100000
		pathToJudge = [1,1,1,1,1,1,1,1,1,1,1,1,1,12,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,23,3,1,1,1,1,1,1,1]
		nextNode = 10000000000
		#The first step of the path should be the trucks current vertex
		aTruck.completePath.append(testVertex)
		removingArray = []
		
		#While their are still stops, because we remove every stop when we add it to truck path
		while len(aTruck.stops) > 0:
			#Make sure this is the longest path and it will be changed with a smaller option
			pathToJudge = [1,1,1,1,1,1,1,1,1,1,1,1,1,12,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,23,3, 2,2,2,2,2,2,2,2,2]
			#For every stop in the truck's list of stops
			array = 0
			for x in aTruck.stops:
				for y in x:
					while False:
						pass				
		
				#don't try to make a path from one vertex to the same one because it won't work, instead create a blank path
				if(testVertex != y):
					quickGraph = graphObject.shortest_path2(testVertex, y, self.Edges)
					skip = 0
					#print("statement", quickGraph)
				else:
					#Don't route from the path we're at to the same one, create a graph of length 0, and skip the loop that trys to find a shorter loop
					quickGraph = []
					#Don't bother looking at other paths
					#Set this node as the shortest path
					nextNode = y
					nextNode = testVertex
					removingArray = x
					#Don't bother finding a shorter path
					skip = 1
	
				#skip is 0 if we haven't found a path of length 0
				if skip == 0:
					
					#quick graph is the path we create from one node to another
					#The path to judge is the current shortest path
					
					#Check if the quick graph is less than the one we're judging
					if (len(quickGraph) < len(pathToJudge)):
						#We found a shorter path, lets see if its valid before we do anything
						#Check if its a key for type needed, only processLines will be in this graph
						if y in aTruck.typeNeeded:
							#If here it is a processLine and needs to check if the truck has the required warehouse materials
							#first what type of resource does it need?
							theTypeNeeded = aTruck.typeNeeded[y]
							
							#See if we have enough in the truck
							if aTruck.loadDict[theTypeNeeded] >= aTruck.amountNeeded[y]:
								#If here we have enough and its a valid path
								nextNode = y
								pathToJudge = quickGraph
								removingArray = x
							else:
								#If we don't have enough materials for the the process line we can't add this to our path yet
								continue
	
						#If on our stop list and not a processs line, its a warehouse
						#Check Load
						else:
							#check to see if the truck has enough capacity
							#Find how much it has now
	
							sum = World.truckLoad(self, aTruck)
							#Now that we have the sum, we can use it to check 
							if (aTruck.capacity >=  (aTruck.totalNeeded[y] + sum)):
								#it has enough capacity to pick up the capacity needed
								#this is a valid path length to check
								nextNode = y
								pathToJudge = quickGraph
								removingArray = x
	
			#end of for loop, so by now we have found the shortest valid path to the vertex we're testing (testVertex)
			#Append the list but don't use the first value, use passer so we don't add the first element twice
			passer = 0
			#We're gonna have to add transporting costs
			transportingCost = World.transportCost(self, aTruck)
			
			sum = World.truckLoad(self, aTruck)
			aTruck.currentLoadSum[0] = 0
			for v in pathToJudge:
				#This if  statement skips the append of the first element in pathToJude
				if passer != 0:
					aTruck.completePath.append(v)
					#We also record the trucks currentLoad at this point (it won't change)
					indexer = len(aTruck.completePath) - 1 #This is the index at the new point
					aTruck.currentLoadSum[indexer] = sum
				else:
					passer = 1
				
				
			#how do we just do the new stuff?
			
			#Make sure the graph has elements or else we skipped the order
			#The complete path is appended every time we have a warehouse or process lines
			
			if (len(aTruck.completePath)!= 0):
				#At the end  of each path portion we have an activity that needs to  be done. We add a arbitrary value of 1 for now
				#The more important part of this is that it saves the index in the path where an action is needed.
				doSomethingHere = len(aTruck.completePath) - 1
				aTruck.timeNeeded[doSomethingHere] = 1
				#We also need to say the capacity may change here
				'''
				currentLoad = World.truckLoad(self, aTruck)
				aTruck.currentLoadSum[doSomethingHere] = currentLoad
				'''
				
			#This will mean its a processLine if it has a typeNeeded
			if nextNode in aTruck.typeNeeded:
	
				#Now we're at the test vertex
				#Decrease the values in the truck
				theTypeNeeded = aTruck.typeNeeded[nextNode]
				pastLoad = aTruck.loadDict[theTypeNeeded]
				nowLoad = pastLoad - aTruck.amountNeeded[nextNode]
				aTruck.loadDict[theTypeNeeded] = nowLoad
	
				
			#If not a processLine its a warehouse
			else:
				#We can pick up the resources now
				resourceType = aTruck.warehouseType[nextNode]
				#Add the resources to the trucks load
				aTruck.loadDict[resourceType] = aTruck.loadDict[resourceType] + aTruck.totalNeeded[nextNode]
	
			
			#Once we add the truck to the path and take the necessary action, remove it so it can't be used again 			
			aTruck.stops.remove(removingArray)
			testVertex =  nextNode
			
	
		#At the very end add a path into the job order destination
		lastPath = graphObject.shortest_path2(nextNode, aTruck.finalNode, self.Edges)
		
		
		sumNow = World.truckLoad(self, aTruck)
		#This just makes sure we add the last path to the complete truck path, and we don't double add the last elemeent
		start = 0
		for numey in lastPath:
			if start == 1:
			 	aTruck.completePath.append(numey)
			 	aTruck.currentLoadSum[len(aTruck.completePath) - 1] = sumNow
			else:
				start = 1


