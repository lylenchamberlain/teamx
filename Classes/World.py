
from  Classes.AbstractWorld import AbstractWorld
from Classes.Animation import Animation

import pygame
import random
import math
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
		self.penatly = 0
		#S
		#Create initial animation objects
		self.truckList = []
		self.ProductionLines = []
		self.loopAmount = 0
		self.totalLateTrucks = 0
		self.totalOnTimeTrucks = 0
		self.lateAmounts = []
		self.transportationCost = 0
		self.trainPaths = []
		self.constructionCost = 0
		
		
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
			
			
		
		
	'''
	1. run simulation
	2. assignNodeDuties (marks which vertexes are universal warehouses and process lines
	3. getInitialTruckLocations (gets the starting vertexes of the trucks)
	4. getNewOrdersForAGivenTime (returns all orders)
	5. drawBackbone (draws the edges and nodes onto the screen)
	6. chooseTruck (chooses the truck to give to the specific new order)
	7. completeTruckReset(sets all truck stats back to default to make sure no previous loads are still on truck)
	8. assignVertexFacts2 (assigns the locations of process lines and warehouses the truck needs to go to.
	9. create_path2(gives the shortest path for two nodes. In this case that means it creates the shortest path to hit all the nodes)
	10. edgeTime (returns the time it takes to go from one node to another
	11. nodeToCoordinates (for animation, allows us to print node in correct spot on screen)
	21. truckIsDone (sets truck to done and empties it so its ready for the next order
	
	'''
	
		
		
		
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
			
			#go through every new order to assign it a node and facts
			for c in newOrders:
				
				skip = 0
				#Choose which truck to use
				currentTruck = World.chooseTruck(self, c)
				#Reset truck to factory default
				World.completeTruckReset(self, currentTruck, currentTruck.currentNode, currentTruck.capacity)

				#Move immediately			
				currentTruck.nextMoveTime =  t
				currentTruck.status = 1
				currentTruck.finalNode = c.finalLocation
				#give it a due date
				currentTruck.dueDate = t + 60				
				
				#This step is complicated but it allows us understand at what point the truck needs to load and unload.
				World.assignVertexFacts2(self, c, currentTruck)	
				#Okay now we assign what each vertex requires
				#Now we have all the stops it will need to do and matneeded, so we will now create a path
				#this is the path the truck will follow until it drops of the order
				World.createPath(self, currentTruck, graphObject, newOrders)
	
			
			for truck in self.truckList:
				
				
				if (truck.status != 4):
					if (t == truck.nextMoveTime):
						
						#make sure we don't graph again, if any path exsts wipe it
						truck.graphingPath = []
						#we just put -10 as a holder to make sure it won't do anythin right now
						truck.nextGraphTime = -10
						truck.graphingIndex = 0
						#IMPORTANT
						#Each truck has a path that it follows. This indicates its ready to travel to the next point in its path
						truck.smallCounter = truck.smallCounter + 1
						#Then represent that the truck moved and mark its current location on the path
						truck.currentNode = truck.completePath[truck.smallCounter]
						#Check if the small counter has a time, if it does that means we need to wait to move for an operation
						if (truck.smallCounter in truck.smallIndexTime) and (truck.currentNode in truck.timeNeeded):
							#if we get here it means that we had a processing line so we need to delay the truck moving until its finished that
							truck.nextMoveTime = t + truck.timeNeeded[truck.currentNode]

						else:
							#if the truck does not have any time at  anode returns t (equivalent to 0)
							truck.nextMoveTime = t
						
						#Takes a while to travel edge to edge
						node2 = truck.completePath[truck.smallCounter]
						node1 = truck.completePath[truck.smallCounter - 1]
						
						#determines the length of the edge the truck is about to travel
						length = World.edgeTime(self,node1, node2, 1)

						#this allows it to move along the edges
						if(length > 1):
							truck.nextGraphTime = t - 5
							#now it has an array
							#World.createGraphArray(self, truck, length, x)
							truck.graphingIndex = 0
												
							#adjust graphing path

							
						#this saves the index from when we just came
						indexToCheck = truck.smallCounter - 1
						try:
							#this adds transportation cost and adds it, it also adjusts move imte
							self.transportationCost = self.transportationCost + (((50 + (5 * length * truck.currentLoadSum[indexToCheck])))* .00001)
							truck.nextMoveTime = truck.nextMoveTime + length
						except:
							#this means there is no cost required, if we get here its because we got a 0 whcih we expect
							self.transportationCost = self.transportationCost + 0
						
						#we randomly move the trucks when they're sitting at a node so that we can see when more than one is at a node
						truck.stayStillX = random.randrange(-1,1) * 3
						truck.stayStillY = 	random.randrange(-1,1) * 3
					
						#Get the coordinates of the node the truck is currently at and graph it
						truckLocation = World.nodeToCoordinate(self,truck.currentNode, self.Verticies)
						truckX = 800 * truckLocation[0] + truck.stayStillX
						truckY = 800 * truckLocation[1] + truck.stayStillY

						#Display the current vertex of the truck
						self.screen.blit(truck.ball, (truckX, truckY))
						
					#move along the edge specified if not at an edge
					elif(t==truck.nextGraphTime):
						truckX = truck.graphingPath[truck.graphingIndex][0] * 800
						truckY = truck.graphingPath[truck.graphingIndex][1] * 800
						truck.graphingIndex = truck.graphingIndex + 1
						self.screen.blit(truck.ball,(truckX,truckY))
					
					#if at a node display it
					else:					
						truckLocation = World.nodeToCoordinate(self,truck.currentNode, self.Verticies)
						truckX = 800 * truckLocation[0] + truck.stayStillY
						truckY = 800 * truckLocation[1] + truck.stayStillY
						#Display the current vertex of the truck
						self.screen.blit(truck.ball, (truckX, truckY))
					
				
				#Got to end of path, so Celebrate!! This blits the party hat
				if (truck.smallCounter == (len(truck.completePath) - 2)):
					truckLocation = World.nodeToCoordinate(self, truck.currentNode, self.Verticies)
					truckX = 500
					truckY = 20
					self.screen.blit(truck.party, (truckX, truckY))
					#set truck to done
					World.truckIsDone(self, truck, t)

			pygame.display.update()	
			self.screen.fill((255,255,255))	
			World.drawScoreboard(self, t)
	
					#This allows us to exit the game if we want
			if World.quitGame(self, fps) == True:
				break				
		#helps us find average late amount
		lateSum = 0
		for x in self.lateAmounts:
			lateSum = lateSum + x
			
		averageLateAmount = lateSum / len(self.lateAmounts)
		
		print("profit", World.calculateProfit(self))	
		print("LATE", self.totalLateTrucks)
		print("ONTIME", self.totalOnTimeTrucks)	
		print("averageLateAmount ", averageLateAmount)
		print("Late amounts", self.lateAmounts)
		print("transportation Costs", self.transportationCost)
		print("late penalty ", self.penalty)
	
	#big method
	def createGraphArray(self, truck, length,  edgeArray ):
		dist = truck.distanceToTravel
		truck.graphingPath = []
		sum = 0
		multiple = truck.distanceToTravel / length
		multiplier = 1
		passer = 1
		
		#this allows us to work with graphing along edges
		while(len(truck.graphingPath) < length):
			#search through the points
			passer = 1
			prevSet = edgeArray[0]
			sum = 0
			for a in edgeArray:
				if (passer== 1):
					passer = 0
				else:
					addOn = World.pythag(self, prevSet, a)
					sum = sum + addOn
					if (sum >= (multiple * multiplier)):
						appending = World.determinePointToAdd(self, truck, addOn, sum, multiplier, multiple, a, prevSet)
						truck.graphingPath.append(appending)
						prevSet = a
						multiplier = multiplier + 1
						break
					prevSet = a
				
		return truck.graphingPath
		
		
	def determinePointToAdd(self,truck,  addOn, sum, multiplier, multiple, destination, previous):
		#this determines where on the edge to put the truck
		#destination and previous are coordinate chunks
		#determine how much over it is
		overLoad = sum - (multiplier * multiple)
		#percentage of length to include
		percentage = (addOn - overLoad) / addOn
		xChunk = destination[0] - previous[0]
		yChunk = destination[1] - previous[1]
		xChunk = xChunk * percentage
		yChunk = yChunk * percentage
		newX = xChunk + previous[0]
		newY = yChunk + previous[1]
		
		return[newX, newY]
		
	#returns an array of data points
	def findEdgeArray(self, startNode, endNode):
		#given two vertexes, find the x and y coordinates that represent the edge
		for a in self.Edges:
			if (a[0] == startNode and a[1] == endNode) or (a[0] == endNode and a[1] == startNode):
				return a[3]
	
	#given a set of x and y coordinates, find the total distance between them
	def totalPythagLength(self, edgeArray):
		previousArray = edgeArray[0]
		sum = 0
		passer = 1
		for p in edgeArray:
			if (passer == 1):
				passer = 0
				continue
			else:
				sum = sum + World.pythag(self, previousArray, p)
				previousArray = p

		return sum
				
	#find the distance between two x and y coordinates	
	def pythag(self, set1, set2):
		#assume you get a set of points (x and y coordinates)
		xsub = set2[0] - set1[0]
		ysub = set2[1] = set1[1]
		total = ((xsub**2) + (ysub**2))**0.5
		return total
		
				
	#given that we're at a specific node, find the coordinates to graph it
	def nodeToCoordinate(self, node, worldVerticies):
		for x in worldVerticies:
			if x[0] == node:
				return (x[1],x[2])
	

	def getGraphingPath(self, path, distance, edgeTime, firstSet, secondSet):
		#Path h= path within an edge
		#distance = total distance a truck with folllow along it
		#edge time = time it takes to do an edge
		#first set and second set give the 
		sum = 0
		multiplier = distance / edgeTime
		nextTarget = multiplier
		multCheck = 0
		passer = 1
		prev = path[0]
		graphingPath = []
		for yt in path:
			#Skip the first set
			if (passer == 1):
				passer = 0
			else:
				shortDist = World.pythag(self, prev, yt)
				sum = sum + shortDist
				
				#See if we've gone over the multiplier length, otherwise keep going for the path
				if (sum >= multiplier):
					#check by how much we've gone over
					overage = World.howMuchOver(self, sum, multiplier)
					#Estimate the percentage of the last path added that is
					percentage = overage / shortDist
					#Find the first set - second set
					addIt = World.findPointToAdd(self, percentage, prev, yt)
					self.graphingPath.append(addIt)
				#add another part of the path	
				else: 
					self.graphingPath.append(yt)
					continue
				
				
				
				prev = yt

		
	def findPointToAdd(self, percentage, prevNode, endNode):
		#This is the total difference in x and y
		minusX = endNode[0] - prevNode[0]
		minusY = endNode[1] - prevNode[1]
		xSegment = minusX * percentage
		ySegment = minusY * percentage
		newNode = [prevNode[0] + xSegment, prevNode[1] + ySegment]
	
		
	def howMuchOver(self, sum, multiplier): 
		return sum - multiplier
		
		
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
		#RETURNS THE DISTANCE
		
		answer =  2000
		
		if loopCount == 3:
			return
		if node1 == node2:
			return 0
		for mine in self.Edges:

			if ((mine[0] == node1) and (mine[1] == node2)) or ((mine[0] == node2) and (mine[1] == node1)):
				answer = mine[2]
				return mine[2]
		loopCount = loopCount + 1
		return 800
		
	def edgePath(self, node1, node2):
		#RETURNS THE MANY X Y COORDINATES OF A PATH
		answer =  2000

		if node1 == node2:
			return 0
		for mine in self.Edges:

			if ((mine[0] == node1) and (mine[1] == node2)) or ((mine[0] == node2) and (mine[1] == node1)):
				answer = mine[3]
				return mine[3]

		return 800
		
	def calculateEdgeDistance(self, paths):
		sum = 0
		prev = [0,0]
		passer = 1
		prev = paths[0]
	
		for at in paths:
			if (passer == 1):
				passer = 0
				continue
			else:
				xdist = at[0] - prev[0]
				ydist = at[1] - prev[1]
				sum = sum + ((xdist**2) + (ydist**2))**0.5
	
		return sum
			
			
		
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
		self.penalty = penalty * .1
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
		
		for x in self.Edges:
			if (x[0] == startNode and x[1] == endNode) or (x[1] == startNode and x[0] == endNode):
				return x[3]
					
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
		self.currentNode = currentVertex
		
		#The following creates a rectangle and  image for the truck
		self.ogball = pygame.image.load("myTrucky.png")
		self.ball = pygame.transform.scale(self.ogball,(25,25))
		self.ballrect = self.ball.get_rect()
		
		self.ogParty = pygame.image.load("party.png")
		self.party = pygame.transform.scale(self.ogParty, (150, 150))
		self.partyrect = self.party.get_rect()
		
		
		self.status = 4 # 1 if moving to starting node, 2 if at starting node, #3 if moving to end node, 4 if done
		#This counter is used to figure out what point on the h the truck is at
		self.smallCounter = 0
		self.finalNode = 1000
		self.processTimes = []
		
		self.currentLoad = "" #String of the job its carrying
		self.thirdListEasy = []
		self.truckPath = []
		self.timeNeeded = []
		self.dict = {}
		self.stops = []
		self.capacity = capacity
		self.loadSize = 0
		self.loadDict = {
		'A' : 0,
		'B' : 0,
		'C' : 0,
		'D' : 0,
		'E' : 0,
		'F' : 0,
		'G' : 0, 
		'H' : 0
		}
		self.totalNeeded = {}
		self.typeNeeded = {}
		self.timeNeeded = {}
		self.amountNeeded = {}
		self.warehouseType = {}
		self.currentPath = []
		self.nextMoveTime = 0
		self.dueDate = 0
		self.completePath = []
		self.truckX = 0
		self.truckY = 0
		self.smallIndexTime = {}
		self.currentLoadSum = {}
		
		self.distanceTraveled = 0
		self.distanceToTravel = 0
		self.distanceMultiplier = 0
		#path of the edges they need to follow
		self.edgePath = 0
		self.graphingPath = []
		self.nextGraphTime = 0
		self.graphingIndex = 0


	def drawScoreboard(self, t):
		text = self.font.render("Time: %02d:%02d"%(t/60, t%60), True, (255, 0, 0), (255, 255, 255))
		textrect = text.get_rect()
		textrect.centerx = 100
		textrect.centery = 30
		#self.screen.fill((255, 255, 255))
		self.screen.blit(text, textrect)
		return
	
		
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
			currentTruck.stops.append(warehousesNeeded)
			
	
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
				
	#Use this for train, vs. assign vertex facts which is for non train		
	def assignTrainVs(self, c, currentTruck):
		#For each step in the new order
		for x in c.productionProcess:
			#material needed in the step
			matNeeded = x['resourceNeeded']
			#Gives index of the process line and warehousewe'll use
			processLineNeeded = World.findProcessLine(self, x['processinLine'])
			warehouseNeeded = World.findWarehouse(self, matNeeded)
			#Make them both stops
			currentTruck.stops.append(processLineNeeded)
			currentTruck.stops.append(warehouseNeeded)
			
	
			#now lets associate this vertex location with the material needed and the amount
			#The following usee the index as the node value of the process line
			#Gives material needed at node
			a = warehouseNeeded
			#currentTruck.timeNeeded[processLineNeeded] = 0
			#For warehouse node value
			currentTruck.timeNeeded[a]= 0
			#Amount of material needed
			currentTruck.totalNeeded[a] = x['materialNeeded[tons]']
			#Specific material needed
			currentTruck.warehouseType[a] = matNeeded
			
			b = processLineNeeded
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
	
	def isTrainTracks(self, node1, node2):
		for i in self.trainPaths:
			if (i[0] == node1 and i[1] == node2) or (i[1] == node1 and i == node2):
				return True
			
		return False
				

				
	def createPath(self, aTruck, graphObject, newOrders):
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
	
	'''
	FOR TRAIN, NOT CAR
	'''
	def runSimulationTrain(self, fps=1, initialTime=5*60, finalTime=23*60):
	
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
	
				#Move immediately			s
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
				World.createTrainPath(self, currentTruck, graphObject, newOrders)
			#Can probably make this a function	
			
			for truck in self.truckList:
				
				
				if (truck.status != 4):
					if (t == truck.nextMoveTime):
						print("TROK", truck.completePath)
						
						truck.smallCounter = truck.smallCounter + 1
						#Increase and then assign current node
						truck.currentNode = truck.completePath[truck.smallCounter]
						#Check if the small counter has a time
						if (truck.smallCounter in truck.smallIndexTime) and (truck.currentNode in truck.timeNeeded):
							truck.nextMoveTime = t + truck.timeNeeded[truck.currentNode] + 2
	
						
						else:
	
							truck.nextMoveTime = t
						
						#Takes a while to travel edge to edge
						
	
						nice = 2
						indexToCheck = truck.smallCounter - 1
						self.transportationCost = 0
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
			
		for xe in self.trainPaths:
			adder =  World.edgeTime(self, xe[0], xe[1], 1)
			self.constructionCost = self.constructionCost + adder
			
			
		print("profit", World.calculateProfit(self)- self.constructionCost)	
		print("LATE", self.totalLateTrucks)
		print("ONTIME", self.totalOnTimeTrucks)	
		print("Late amounts", self.lateAmounts)
		print("transportation Costs", self.transportationCost)
		print("building costs", self.constructionCost)
		
				
	'''
	FOR TRAIN  ONLY
	'''
	
	def createTrainPath(self, aTruck, graphObject, newOrders):
			
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
							print(aTruck.typeNeeded)
							
						
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
	
			aTruck.completePath.append(nextNode)
			#We also record the trucks currentLoad at this point (it won't change)
			indexer = len(aTruck.completePath) - 1 #This is the index at the new point
			aTruck.currentLoadSum[indexer] = sum
	
				
				
			#Make sure the graph has elements or else we skipped the order
			#The complete path is appended every time we have a warehouse or process lines	
			#At the end  of each path portion we have an activity that needs to  be done. We add a arbitrary value of 1 for now
			#The more important part of this is that it saves the index in the path where an action is needed.
			doSomethingHere = len(aTruck.completePath) - 1
			aTruck.timeNeeded[doSomethingHere] = 1

				
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
		
		sumNow = World.truckLoad(self, aTruck)
		#This just makes sure we add the last path to the complete truck path, and we don't double add the last elemeent
	
		aTruck.completePath.append(aTruck.finalNode)
		aTruck.currentLoadSum[len(aTruck.completePath) - 1] = sumNow
		
		for ak in range(0, len(aTruck.completePath)- 2):
			if World.isTrainTracks(self, aTruck.completePath[ak], aTruck.completePath[ak + 1]):
				continue
			else:
				self.constructionCost =  self.constructionCost + 2
				self.trainPaths.append([aTruck.completePath[ak], aTruck.completePath[ak + 1]])
				print(self.trainPaths)
			
	

