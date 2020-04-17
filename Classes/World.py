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

		#Create initial animation objects
		self.truckList = []
		self.ProductionLines = []
		self.loopAmount = 0
		
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
		#print("LOCATION", World.findWarehouse(self, 'A'))
		'''
		This will give you a list of ALL cars which are in the system
		'''
		self.trucks = self.getInitialTruckLocations()
		for i,t in enumerate(self.trucks):
			print("vehicle %d: %s"%(i, str(t)))
		'''
		We will run a simulation where "t" is the time index
		'''
			
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
				
			
			text = self.font.render("Time: %02d:%02d"%(t/60, t%60), True, (255, 0, 0), (255, 255, 255))
			textrect = text.get_rect()
			textrect.centerx = 100
			textrect.centery = 30
			#self.screen.fill((255, 255, 255))
			self.screen.blit(text, textrect)


 			#Draw Vertices onto the screen
			for item in range(len(self.Verticies)):
				pygame.draw.rect(self.screen,(0,0,0),(800*self.Verticies[item][1],800*self.Verticies[item][2],10,10))

			#Draws Edges onto the screen
			for x in range(len(self.Edges)):
				#Iterate through all the points of path
				for y in range(len(self.Edges[x][3]) - 1):
					pygame.draw.line(self.screen,(90,200,90), (self.Edges[x][3][y][0]*800, self.Edges[x][3][y][1]*800), (self.Edges[x][3][y+1][0]*800, self.Edges[x][3][y+1][1]*800) , 4)
				
			graphObject = Graph()
		
			for c in newOrders:
				
				#Figure out the total capacity that is needed
				totalNeeded = 0
				for theLine in c.productionProcess:
					totalNeeded = totalNeeded + theLine['materialNeeded[tons]'] 
				#Now that we know total needed grab a truck
				for aTruck in self.truckList:
					if (aTruck.capacity >= totalNeeded and aTruck.status == 4):
						currentTruck = aTruck
						break
							
				#Move immediataely				
				currentTruck.nextMoveTime =  t
				currentTruck.status = 1
				currentTruck.finalNode = c.finalLocation
				
				#Add everything to the truck path
				#Find each warehouse and line
				for x in c.productionProcess:
					matNeeded = x['resourceNeeded']
					#Gives index of the process line we'll use
					processLineNeeded = World.findProcessLine(self,x['processinLine'])
					warehouseNeeded = World.findWarehouse(self, matNeeded)
					#Make them both stops
					currentTruck.stops.append(processLineNeeded)
					currentTruck.stops.append(warehouseNeeded)
					#now lets associate this vertex location with the material needed and the amount
					currentTruck.typeNeeded[processLineNeeded] = matNeeded
					currentTruck.amountNeeded[processLineNeeded] = x['materialNeeded[tons]']
					currentTruck.totalNeeded[warehouseNeeded] = x['materialNeeded[tons]']
					currentTruck.warehouseType[warehouseNeeded] = matNeeded
					
				#Now we have all the stops it will need to do and matneeded, so we will now create a path
				World.createPath(self, currentTruck, graphObject)
				
			for truck in self.truckList:
				if (truck.status != 4):

					if (t == truck.nextMoveTime):
							truck.smallCounter = truck.smallCounter + 1
							truck.nextMoveTime = t + 25
					truck.currentNode = truck.currentPath[truck.smallCounter]

					truckLocation = World.nodeToCoordinate(self,truck.currentNode, self.Verticies)
					truckX = 800 * truckLocation[0]
					truckY = 800 * truckLocation[1]
					#Display the current vertex of the truck
					self.screen.blit(truck.ball, (truckX, truckY))
					
					#Got to end of path
					if (truck.smallCounter >= len(truck.currentPath) - 2):
						truck.status = 4
				
			
			pygame.display.update()	
			self.screen.fill((255,255,255))	
			'''
					if (currentTruck.currentNode != currentWarehouse):
						#Make path from currentNode to warehouse
						currentTruck.truckPath.append( graphObject.shortest_path2(currentTruck.currentNode,currentWarehouse,self.Edges)	)			
					#Make path to line
					currentTruck.truckPath.append(graphObject.shortest_path2(currentWarehouse, currentLine, self.Edges))
				
					#Make a path from final line to final node
					currentTruck.truckPath.append(graphObject.shortest_path2(currentLine, c.finalLocation, self.Edges))
					
	
					if truck.status != 4 and truck.nextMoveTime == t:	
						#truck.nextMoveTime = t + 6
	
						#Are we at the end of small array?
						if truck.smallCounter == (len(truck.truckPath[truck.bigCounter]) - 1):
							
							#Are we at the final node?
							if (truck.bigCounter == len(truck.truckPath) - 1):
								#BReak out, we're done.
								truck.smallCounter = 0
								truck.bigCounter = 0
								truck.status = 4
								truck.currentLoad = ""
								truck.processTimes = []
								truck.nextMoveTime = 0
								
							#If so, we want to go to the next big path and reset small counter
							#Careful, I think we might double count a vertex when changing nodes
							
							else:
								truck.bigCounter = truck.bigCounter + 1
								truck.smallCounter = 0
								
						
						else:
							truck.smallCounter = truck.smallCounter + 1
	
						truck.currentNode = truck.truckPath[truck.bigCounter][truck.smallCounter]
	
						#We assign truck currentNod
						for dict in truck.dict:
							if (truck.currentNode == dict):
								#We need to add a time
								truck.nextMoveTime = t + truck.dict[truck.currentNode]
							else:
								truck.nextMoveTime = t + 1
							
						
						#Start animation
						if truck.status != 4:	
							truckLocation = World.nodeToCoordinate(self,truck.currentNode, self.Verticies)
							truckX = 800 * truckLocation[0]
							truckY = 800 * truckLocation[1]
							#Display the current vertex of the truck
							self.screen.blit(truck.ball, (truckX, truckY))
					pygame.display.update()		
					
						
				#End of for loop for trucks, my animation trick for third list now		
					
						#Make a route from current vertex to warehouse
						
						#Append it to current truck path
						#Make a route from warehouse to processLine
						#append it to current truck path
						
				#UPDate
	
						
	
			
	
	
				#Goes through all the new orders. If no new orders we don't go into this for loop
				for x in newOrders:
					
					#Create two random vertexes for order to travel 
					orderVertexStart = World.getRandomVertex(self)
					orderVertexEnd = World.getRandomVertex(self)
					#They can't be the same because that wouldn't makes sense logically for an order to go to the same place
					while orderVertexEnd == orderVertexStart:
						orderVertexEnd = World.getRandomVertex(self)
					
					#Gives the truck a path from where to pick up the order to where to drop it off
					self.truckList[self.orderTracker].currentPath2 = graphObject.shortest_path2(orderVertexStart,orderVertexEnd,self.Edges)				
					#If the truck is not already at the place to pick up the job, create a path from its location to the start
					if self.truckList[self.orderTracker].currentNode != orderVertexStart:
						self.truckList[self.orderTracker].currentPath = graphObject.shortest_path2(self.truckList[self.orderTracker].currentNode, orderVertexStart, self.Edges)
					#If the truck is at the location, only use the path from the job pick up to drop off
					else:
						 self.truckList[self.orderTracker].currentPath =  self.truckList[self.orderTracker].currentPath2
					
					#Set status to 1 to indicate the truck is moving to the starting node
					self.truckList[self.orderTracker].status = 1
	
					#Set moveTime to now so it'll immediately execute
					self.truckList[self.orderTracker].nextMoveTime = t	
					#Store the fact that the truck is storing a load
					self.truckList[self.orderTracker].currentLoad = x		
					#Store the drop off node as final destination
					self.truckList[self.orderTracker].nodeFinalDestination = orderVertexEnd
					#Increment the cycle through the truckList
					#This allows us to assign trucks sequentially
					self.orderTracker = self.orderTracker + 1
					#If this counter is out of index reset it to 0
					if self.orderTracker >= len(self.truckList):
						self.orderTracker = 0
						
				#This for loop finds out where a truck is in relation to paths its been given to it		
				for aTruck in self.truckList:
					
					aTruck.departureNode = aTruck.currentNode
					#If status is not done and the truck is scheduled to move enter this loop
					if t == aTruck.nextMoveTime and aTruck.status != 4:
						#Counter to tell us which element in the path to access
						aTruck.counter=  aTruck.counter + 1
						#Schedule a new movement time so we can move it in the future
						aTruck.nextMoveTime = t + 1
					
						#This length represents the index of the last element in a list
						myLength = len(aTruck.currentPath) - 1
						 
						#If we're at the final point in the path, go into this loop
						if aTruck.currentNode == aTruck.currentPath[myLength]:
							
							#If the truck is at the drop-off point and this is its final location, go into loop
							if aTruck.currentNode ==  aTruck.nodeFinalDestination:
								#We don't want it to move again (until assigned) so we set move time to 0
								aTruck.nextMoveTime = 0
								#status of 4 means done
								aTruck.status = 4
								#No longer has a job so currentLoad is reset
								aTruck.currentLoad = ""
								#Resets truck's counter to 0 so wehn the truck is called again it has a fresh slate
								aTruck.counter = 0
								
								
							#If we go here its because we're at the end of our path but not at the node we want (finalDestinationNode)
							#This means we're at the node where the path to the object starts
							else:
								#We're going to have to make a path from currentVertex to final node destination
								aTruck.currentPath = aTruck.currentPath2
								#status of 2 means at start node
								aTruck.status = 2
								#Reset counter to start at first index of our new list
								#We know that truck is incremented above before used, meaning the first index of the second list is ignored
								#We want this because the first element of the second list is the node we are already at
								aTruck.counter = 0
						
						#This indicates we're not at the end of our path, so using same path go to next element
						else:
							aTruck.currentNode = aTruck.currentPath[aTruck.counter]
							
				#print out our trucks at their current index, this works. But lets get fancy
				#for t in self.truckList:
			
				#For now only display if not done (Status is not 4)
				#if t.status != 4:
				if True:
					#For now we don't want any speed
					t.speedX = 0
					t.speedY = 0
					t.ballrect = t.ballrect.move(t.speedX, t.speedY)
					#Takes the current vertex and changes that into coordinates
					truckLocation = World.nodeToCoordinate(self,t.currentNode, self.Verticies)
					#Scales the coordinates to fit our grid
					truckX = 800 * truckLocation[0]
					truckY = 800 * truckLocation[1]
					#Display the current vertex of the truck
					self.screen.blit(t.ball, (truckX, truckY))
				
					
				#If its done delete the animation (we move off screen because I don't know how to unblit)
				#else:
				#	self.screen.blit(t.ball, (2000,2000))
				
				#First let's split up each necessary edge into an edge of 20
				#Max data points = 34 so lets use 35
				
				#This actually resets t (not what we want, but it works
				for u in self.truckList:
					
					if u.status != 4:
						#Quick fix for index problem
						if len(u.currentPath) != (u.counter+1):
	
	
							if u.counter != 0:
								thirdList = World.edgeToList(self, u.currentPath[u.counter - 1], u.currentPath[u.counter])
							else: 
								thirdList = World.edgeToList(self,u.currentPath[u.counter], u.currentPath[u.counter+1])
							testCount = 0
							
							u.thirdList = thirdList
							
							for p in u.thirdList:
								#t.thirdListEasy.append((p[0],p[1]))
								u.thirdListEasy.append((p[0],p[1]))
				
				
				#Now print out the trucks using third list
				
				for ww in self.truckList:
					
					for pp in ww.thirdListEasy:
						
					
						#This splits up the smalles length to show movement by splitting it into ten parts
						if len(ww.thirdListEasy) < 3:
							#The two values are the following
							originalX1 = ww.thirdListEasy[0][0]
							originalY1 = ww.thirdListEasy[0][1]
							originalX2 = ww.thirdListEasy[1][0]
							originalY2 = ww.thirdListEasy[1][1]
							
							xFactor = (originalX1 - originalX2)/10
							yFactor = (originalY1 - originalY2) /10
							
							#Now create a new list!
							for i in range(10):
								addOnX = originalX2 + xFactor * i
								addOnY = originalY2 + yFactor * i
								#addOnX = xFactor
								#addOnY = yFactor 
								ww.thirdListEasy.insert(0, (addOnX, addOnY))
							
							
							#print("WWW", ww.thirdListEasy)
							
							break
							#print("CHANGW", ww.thirdListEasy)
							
							
						
				
				
				for i in range(0,35):
					#pygame.display.update()
					#This works but it does it all at once
					#self.screen.fill((255,255,255))
					
					#self.screen.blit(self.screen, t.ballrect, (x, y), 10)
					#self.screen.blit(yy.ball, (x,y))
					#Draw Vertices onto the screen
	
			
			self.screen.fill((255,255,255))

			for item in range(len(self.Verticies)):
				pygame.draw.rect(self.screen,(0,0,0),(800*self.Verticies[item][1],800*self.Verticies[item][2],10,10))
			
			#Draws Edges onto the screen
			for x in range(len(self.Edges)):
				#Iterate through all the points of path
				for y in range(len(self.Edges[x][3]) - 1):
					pygame.draw.line(self.screen,(90,200,90), (self.Edges[x][3][y][0]*800, self.Edges[x][3][y][1]*800), (self.Edges[x][3][y+1][0]*800, self.Edges[x][3][y+1][1]*800) , 4)
			'''
			text = self.font.render("Time: %02d:%02d"%(t/60, t%60), True, (255, 0, 0), (255, 255, 255))
			textrect = text.get_rect()
			textrect.centerx = 100
			textrect.centery = 30
			self.screen.blit(text, textrect)
			
					
				#This allows us to exit the game if we want
			if World.quitGame(self, fps) == True:
				break	
		''''''
					
	
							
		


	
	#Give it a vertex ID (its unique identifier) this will return the x and y value in a tuple
	def nodeToCoordinate(self, node, worldVerticies):
		print("!@#", node)
		for x in worldVerticies:
			if x[0] == node:
				return (x[1],x[2])
		
		
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
				
	def createPath(self, aTruck, graphObject):
		
		testVertex = aTruck.currentNode
		shortestLength = 100000
		pathToJudge = [1,1,1,1,1,1,1,1,1,1,1,1,1,12,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,23,3]
		aTruck.currentPath.append(aTruck.currentNode)
		nextNode = 0
		
		
		while len(aTruck.stops) > 0:
			pathToJudge = [1,1,1,1,1,1,1,1,1,1,1,1,1,12,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,23,3]

			for x in aTruck.stops:
				#Go through all the stops
				if(testVertex != x):
					quickGraph = graphObject.shortest_path2(testVertex, x, self.Edges)

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
				aTruck.currentPath.append(nextNode)
				print("LOAD", aTruck.loadDict)
			#else its a warehouse
			else:
				#We can pick up the resources now
				resourceType = aTruck.warehouseType[nextNode]
				#Add the resources to the trucks load
				aTruck.loadDict[resourceType] = aTruck.loadDict[resourceType] + aTruck.totalNeeded[nextNode]
				#this is now a confirmed next destination, so add it
				aTruck.currentPath.append(nextNode)
				testVertex = nextNode
				print("LOAD", aTruck.loadDict)
			
			print("NEXT", aTruck.stops, nextNode, pathToJudge)
			if len(aTruck.stops) == 1:
				aTruck.stops.clear()
			else:
				aTruck.stops.remove(nextNode)			
			
		aTruck.currentPath.append(aTruck.finalNode)
			
			
					
					
					
					
					
					
			#It is done with the loop, set truck status to 4
		aTruck.status == 4
			

	def findLoadSum(self, aTruck):
		total =  0
		for x in aTruck.loadDict:
			total = total + aTruck.loadDict[x]
		return total
				
	
		
		

