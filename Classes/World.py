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

		#Create initial animation objects
		self.truckList = []
		zz = 0
		for i in self.trucks:

			#Determine coordinates of that node
			for x in self.Verticies:
				#This is the Vertex the truck starts at
				startingNode = i.currentVertex
				currentVertex = i.currentVertex
				#print("myTest", x[1])
				if x[0] == startingNode:
					startingX = x[1] * 800
					startingY = x[2] * 800
					break

					
			myAnimate = Animation(startingX, startingY, currentVertex)
			self.truckList.append(myAnimate)
			zz = zz + 1
			

				#print("FINAL lsit", self.truckList)
		
	def generateTruckList(self):
		x = 0
		truckList = []
		#classObject = Animation()

		
		for i in self.trucks:
			#myAnimate = Animation.generateRandomVerticies
			#truckList.append(myAnimate)
			#truckList[x].speed = [0,0]
			
			#truckList[x].currentPosition = i.currentVertex
			x += 1
		self.truckList = truckList
		return
			
			
	def runSimulation(self, fps=1, initialTime=5*60, finalTime=23*60):

		'''
		
		This will give you a list of ALL cars which are in the system
		'''
		self.trucks = self.getInitialTruckLocations()
		for i,t in enumerate(self.trucks):
			print("vehicle %d: %s"%(i, str(t)))
			
			
		print("****", self.Edges)


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
			
			text = self.font.render("Time: %02d:%02d"%(t/60, t%60), True, (255, 0, 0), (255, 255, 255))
			textrect = text.get_rect()
			textrect.centerx = 100
			textrect.centery = 30
			self.screen.fill((255, 255, 255))
			self.screen.blit(text, textrect)
 			

			#This is our print
			#print Vertices
			for item in range(len(self.Verticies)):
				pygame.draw.rect(self.screen,(0,0,0),(800*self.Verticies[item][1],800*self.Verticies[item][2],10,10))
				#print(self.Verticies[item])

			#Prints edges
			for x in range(len(self.Edges)):
				#Iterate through all the points of path
				for y in range(len(self.Edges[x][3]) - 1):
					pygame.draw.line(self.screen,(90,200,90), (self.Edges[x][3][y][0]*800, self.Edges[x][3][y][1]*800), (self.Edges[x][3][y+1][0]*800, self.Edges[x][3][y+1][1]*800) , 4)

			#Get a list of the shortest path
			myShortest = []

			graphObject = Graph()
			myShortest = graphObject.shortest_path2(1,2, self.Edges)
			
			#Eventually this should go into for loop, but lets test it
			self.truckList[0].finalNodeDestination = 2
			self.truckList[0].destination = 2
			self.truckList[0].currentPath = graphObject.shortest_path2(1,2, self.Edges)
			
			#We need to always first make a path from where it is to vertex
			self.truckList[0].currentPath = graphObject.shortest_path2(37,1, self.Edges)
			self.truckList[0].currentPath2 = graphObject.shortest_path2(1,2,self.Edges)

			
			#Just for a test we want to make sure it moves
			if self.truckList[0].nextMoveTime == 0:
				#This should be t + 60 but we're gonna shorten it
				self.truckList[0].nextMoveTime = t + 6
			
			
			print("ERE ", self.truckList[0].currentNode)
			print("SHORTY ", self.truckList[0].currentPath)
			print("TTT", t, self.truckList[0].nextMoveTime)
			
			#If we're at the start node we need a new path
			if self.truckList[0].status == 2:
				self.truckList[0].currentPath = self.truckList[0].currentPath2
			
			
			#Decide if a minute has passed
			if t == self.truckList[0].nextMoveTime:
				#This counter tells us where we are at in the array
				self.truckList[0].counter = self.truckList[0].counter + 1
				#This sets the move time again 
				#This should be t + 60 but for time purposes we shortened it
				self.truckList[0].nextMoveTime = t + 8
				#Test if we're at end of the path
				if self.truckList[0].currentNode == self.truckList[0].nodeDestination:
					
					#check if we're where we want to be
					if self.truckList[0].currentNode ==  self.truckList[0].finalNodeDestination:
						nextMoveTime = 0
						#status of 4 means done
						self.truckList[0].status = 4
					#This means we're at the start node and need to go to end node
					else:
						#We're gonna have to make a path from currentVertex to final node destination
						self.truckList[0].currentPath = graphObject.shortestPath(22,3,self.Edges)
						#status of 2 means at start node
						self.truckList[0].status = 2
						print(" Changed status to 2")
						#Resetcounter to start at firstNode
						#This is a weird counter
						self.truckList[0].counter = 0
						
				#If we're still traveling on the same path
				else:
					print("Counter = ", self.truckList[0].coounter)
					self.truckList[0].currentNode = self.truckList[0].currentPath[self.truckList[0].counter]
			#End of test		
			
			#list of verticies
			pleaseVert = self.Verticies
			print(pleaseVert, "please Vert")
			#Print out all in truckList
			#Prints out all the speeds
			for t in self.truckList:
				'''
				#newSpeed = World.createSpeed(t, t.departureNode, t.nodeDestination, pleaseVert)
				'''
				#This moves it with a given speed
				newSpeed = [0,0]
				t.speedX = newSpeed[0]
				t.speedY = newSpeed[1]
				t.ballrect = t.ballrect.move(t.speedX, t.speedY)
				self.truckTop = t.ballrect.top
				self.truckLeft = t.ballrect.left
				self.screen.blit(t.ball, t.ballrect)
				
				
				

			#I don't know what this does
			for x in self.trucks:
			
				for y in self.Verticies:
				# Find the index of the node position we care about
					
					if x.VehicleID == y[0]:
						x.currentVertex == y[0]
						#pygame.draw.rect(self.screen,(255,0,0),(800*y[1],800*y[2],40,40))
			

     
			pygame.display.update()	
	
			gameExit = False			
			
			for event in pygame.event.get():
				
				if event.type == pygame.QUIT:
					gameExit = True
					pygame.quit()
					
				
				
			self.clock.tick(fps)
			if gameExit == True:
				break
	
	
	def createSpeed(self,firstNode,secondNode, worldVerticies):
		
		firstNodeCoordinates = World.nodeToCoordinate(self, firstNode, worldVerticies)
		secondNodeCoordinates =  World.nodeToCoordinate(self, secondNode, worldVerticies)

		#newSpeed[0] = secondNodeCoordinates - firstNodeCoordinates
		newSpeed = [0,0]
		xDir = secondNodeCoordinates[0] - firstNodeCoordinates[0] * 5
		yDir = (secondNodeCoordinates[1] - firstNodeCoordinates[1])* 5
		self.speed = [xDir,yDir]
		return [xDir,yDir]
	
		
	def nodeToCoordinate(self, node, worldVerticies):
		
		for x in worldVerticies:
			if x[0] == node:
				return (x[1],x[2])
			
			
			
	def pathFollowing(self):
		#the node its trying to get to 
		#The node its at
		#Move at everey minute
		pass
				
				
				
	def decideIfArrived(self):
		#
		#Keep the same path, and go to the next node in
		pass
	
	def decideIfAtStart(self):
		#Get a new shortest path
		pass
	def decideIfEnded(self):
		#Speed should go to zero
		
		pass

