from  Classes.AbstractWorld import AbstractWorld
from Classes.Animation import Animation

import pygame
import random
from Graph import Graph
from array import array
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
		
		for i in self.trucks:
			#Go through all the verticies to determine which one the struck is at
			for x in self.Verticies:
				#This is the Vertex the truck starts at
				startingNode = i.currentVertex
				#This looks for the vertex identifier in the verticies list and returns x and y value for it
				if x[0] == startingNode:
					startingX = x[1] * 800
					startingY = x[2] * 800
					break
			
			#Create an animation object (it's a truck picture) with the node identifier that it starts at
			myAnimate = Animation(startingNode)
			self.truckList.append(myAnimate)
			
					
	def runSimulation(self, fps=1, initialTime=5*60, finalTime=23*60):

		'''
		This will give you a list of ALL cars which are in the system
		'''
		self.trucks = self.getInitialTruckLocations()
		for i,t in enumerate(self.trucks):
			print("vehicle %d: %s"%(i, str(t)))
		'''
		We will run a simulation where "t" is the time index
		'''
		for t in range(initialTime,finalTime):	
			print("\n\n Time: %02d:%02d"%(t/60, t%60))

			# each minute we can get a few new orders
			newOrders = self.getNewOrdersForGivenTime(t)
			print("New orders:")
			#Let's graph the truck movements here
			
			for c in newOrders:
				print(c)
				#I think we should add paths here for specific vehicles
			
			text = self.font.render("Time: %02d:%02d"%(t/60, t%60), True, (255, 0, 0), (255, 255, 255))
			textrect = text.get_rect()
			textrect.centerx = 100
			textrect.centery = 30
			self.screen.fill((255, 255, 255))
			self.screen.blit(text, textrect)
 			
 			#Draw Vertices onto the screen
			for item in range(len(self.Verticies)):
				pygame.draw.rect(self.screen,(0,0,0),(800*self.Verticies[item][1],800*self.Verticies[item][2],10,10))

			#Draws Edges onto the screen
			for x in range(len(self.Edges)):
				#Iterate through all the points of path
				for y in range(len(self.Edges[x][3]) - 1):
					pygame.draw.line(self.screen,(90,200,90), (self.Edges[x][3][y][0]*800, self.Edges[x][3][y][1]*800), (self.Edges[x][3][y+1][0]*800, self.Edges[x][3][y+1][1]*800) , 4)
				
				#Create an object to Access functions in the graph class
				
			#screen.blit(background_surface, (0, 0))

			graphObject = Graph()

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
			'''for t in self.truckList:
				
				#For now only display if not done (Status is not 4)
				if t.status != 4:
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
				else:
					self.screen.blit(t.ball, (2000,2000))
			'''
			#First let's split up each necessary edge into an edge of 20
			#Max data points = 34 so lets use 35
			
			#This actually resets t (not what we want, but it works
			for t in self.truckList:
				if t.status != 4:
					#Quick fix for index problem
					if len(t.currentPath) != (t.counter+1):

						

						if t.counter != 0:
							thirdList = World.edgeToList(self, t.currentPath[t.counter - 1], t.currentPath[t.counter])
						else: 
							thirdList = World.edgeToList(self,t.currentPath[t.counter], t.currentPath[t.counter+1])
						testCount = 0
						
						t.thirdList = thirdList
						
						for p in t.thirdList:
							#t.thirdListEasy.append((p[0],p[1]))
							t.thirdListEasy.append((p[0],p[1]))
			
			
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
						
						
					
			
			
			for yy in self.truckList:
				
				if yy.status != 4:

				#	print("THIRD", yy.thirdListEasy)
					for kk in yy.thirdListEasy:
						
						
						x = kk[0] * 800
						y = kk[1] * 800
						#self.screen.blit(self.screen, t.ballrect, (x, y), 10)
						self.screen.fill((255,255,255))
						self.screen.blit(t.ball, (x,y))
						'''This is all very bad but it works'''
						 #Draw Vertices onto the screen
						for item in range(len(self.Verticies)):
							pygame.draw.rect(self.screen,(0,0,0),(800*self.Verticies[item][1],800*self.Verticies[item][2],10,10))
			
						#Draws Edges onto the screen
						for x in range(len(self.Edges)):
							#Iterate through all the points of path
							for y in range(len(self.Edges[x][3]) - 1):
								pygame.draw.line(self.screen,(90,200,90), (self.Edges[x][3][y][0]*800, self.Edges[x][3][y][1]*800), (self.Edges[x][3][y+1][0]*800, self.Edges[x][3][y+1][1]*800) , 4)
							
						#text = self.font.render("Time: %02d:%02d"%(t/60, t%60), True, (255, 0, 0), (255, 255, 255))
						#textrect = text.get_rect()
						#textrect.centerx = 100
						#textrect.centery = 30
						#self.screen.fill((255, 255, 255))
						#self.screen.blit(text, textrect)
						'''end of very bad screen redraw'''
				#Create an object to Access functions in the graph class
				
						#yy.ballrect = yy.ballrect.move(yy.speedX, yy.speedY)
						#self.screen.blit(self.screen, (x, y), pygame.Rect(x, y, 62, 62))
						pygame.display.update()


						

					

			'''#Now display, just got to figure out type of third list
			for tt in self.truckList:
						
				for zz in tt.thirdList:		
					truckX = zz[0] * 800
					truckY = zz[1] * 800
					self.screen.blit(t.ball, (truckX, truckY))
			'''
		
					
				

			'''
			for t in self.truckList:
				if t.status != 4:
					#Quick fix for index problem
					if len(t.currentPath) == (t.counter + 1):
						t.counter = t.counter - 1
					#Get that list of all the points it has to pass	
					thirdList = []
					thirdList = World.edgeToList(self, t.currentNode, t.currentPath[t.counter + 1])
					
					for z in thirdList:
						truckX = z[0] * 800
						truckY = z[1] * 800
						self.screen.blit(t.ball, (truckX, truckY))
						
			'''			
						
						
						
			#update display	
			pygame.display.update()	

			#This allows us to exit the game if we want
			gameExit = False			
			for event in pygame.event.get():
				
				if event.type == pygame.QUIT:
					gameExit = True
					pygame.quit()
					
				
				
			self.clock.tick(fps)
			if gameExit == True:
				break
	
	
	#This is not used right now. Its a function that gives a proper animation speed based on two vertexes so I'll keep it in for now
	'''def createSpeed(self,firstNode,secondNode, worldVerticies):
		
		firstNodeCoordinates = World.nodeToCoordinate(self, firstNode, worldVerticies)
		secondNodeCoordinates =  World.nodeToCoordinate(self, secondNode, worldVerticies)

		#newSpeed[0] = secondNodeCoordinates - firstNodeCoordinates
		newSpeed = [0,0]
		xDir = secondNodeCoordinates[0] - firstNodeCoordinates[0] * 5
		yDir = (secondNodeCoordinates[1] - firstNodeCoordinates[1])* 5
		self.speed = [xDir,yDir]
		return [xDir,yDir]
	'''
	
	#Give it a vertex ID (its unique identifier) this will return the x and y value in a tuple
	def nodeToCoordinate(self, node, worldVerticies):
		
		for x in worldVerticies:
			if x[0] == node:
				return (x[1],x[2])
			
			
	#Returns a value for random vertex. It will only return the integer unique identifying value
	def getRandomVertex(self):
		#Choose a random Vertex from the Verticies
		randomVertex = random.choice(self.Verticies)
		randomVertexValue = randomVertex[0]
		return randomVertexValue 
	
	def edgeToList(self, startNode, endNode):
		
		#print("Start and end node ", startNode, endNode)
		for x in self.Edges:
			
	
			if (x[0] == startNode and x[1] == endNode) or (x[1] == startNode and x[0] == endNode):
				#print("X3", x[3])
				#print(self.Edges)
				#print(x[3])
				#print(type(x[3]))
				return x[3]
			
		print("ERROR")
		
		

