from  Classes.AbstractWorld import AbstractWorld
from Classes.Animation import Animation

import pygame
import random
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
			'''we moved this to the end
			myAnimate = Animation()
			self.truckList.append(myAnimate)
			'''
			#self.truckList[x].value = x
			#i current position should enter node its at
			
			#Determine node that it start at initially
			#For now we'll give it a random starting node
			 
			#x = x + 1
			print("Truck ", i.VehicleID)
			#Determine coordinates of that node
			for x in self.Verticies:
				#This is the Vertex the truck starts at
				startingNode = i.currentVertex
				#print("myTest", x[1])
				if x[0] == startingNode:
					startingX = x[1] * 800
					startingY = x[2] * 800
					break

					
			myAnimate = Animation(startingX, startingY)
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
			
			
		print("****", self.Edges[0])


			#This is test that truckList works
		for i in self.truckList:
			print("MYMY value ")#, i.value)
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


			
			#Lets try printing all our trucks, this is an example
			#self.ballrect = self.ballrect.move(self.speedX, self.speedY)
			
			#This moves the truck at a speed
			#self.screen.blit(self.ball,self.ballrect)
			
			#list of verticies
			pleaseVert = self.Verticies
			print(pleaseVert, "please Vert")
			#Print out all in truckList
			#Prints out all the speeds
			for t in self.truckList:
				
				newSpeed = World.createSpeed(t, t.startingFirstNode, 40, pleaseVert)
				#Takes the speed output from the create speed method
				t.speedX = newSpeed[0]
				t.speedY = newSpeed[1]
				t.ballrect = t.ballrect.move(t.speedX, t.speedY)

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
			
	def decideIfArrived(self):
		pass

