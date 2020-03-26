from  Classes.AbstractWorld import AbstractWorld
#from Classes.Animation import Animation

import pygame
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

		self.ogball = pygame.image.load("myTrucky.png")
		self.ball = pygame.transform.scale(self.ogball,(50,50))
		self.ballrect = self.ball.get_rect()
		self.ballrect = self.ballrect.move(350,350)
		self.truckList = []
		self.speed = []
		
		#self.truckList = listCreate(self)
		#x = 0
		#self.truckList = []
		#Animation.generatesRandomVerticies(self.trucks)
		#self.truckList = Animation.generateTrucklist
		'''
		for i in self.trucks:
			myAnimate = Animation()
			self.truckList.append(myAnimate)
			self.truckList[x].speed = [0,0]
			
			self.truckList[x].currentPosition = i.currentVertex
			
			
		x+=1
		'''

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

					
			'''
			#Lets try to print out our trucks
			for x in self.truckList:
				self.screen.blit(self.ball,self.ballrect)
				print("MINEY", x)
				self.ballrect = self.ballrect.move(x.speed)
			'''
			
			
			for x in self.trucks:
				
				for y in self.Verticies:
				# Find the index of the node position we care about
					
					if x.VehicleID == y[0]:
						x.currentVertex == y[0]
						#pygame.draw.rect(self.screen,(255,0,0),(800*y[1],800*y[2],40,40))
			
			pleaseVert = self.Verticies
			World.createSpeed(self, 1, 40, pleaseVert)
			#self.speed = [0,1]
			#This sets the position
			self.ballrect = self.ballrect.move(self.speed)
			
			#This moves the truck at a speed.

			self.screen.blit(self.ball,self.ballrect)
     
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
		
		print(firstNode)
		firstNodeCoordinates = World.nodeToCoordinate(self, firstNode, worldVerticies)
		secondNodeCoordinates =  World.nodeToCoordinate(self, secondNode, worldVerticies)

		#newSpeed[0] = secondNodeCoordinates - firstNodeCoordinates
		newSpeed = [0,0]
		xDir = secondNodeCoordinates[0] - firstNodeCoordinates[0] * 50
		yDir = (secondNodeCoordinates[1] - firstNodeCoordinates[1])* 50
		print("WWW.", newSpeed)
		self.speed = [xDir,yDir]
		return [xDir,yDir]
		
	def nodeToCoordinate(self, node, worldVerticies):
		
		for x in worldVerticies:
			if x[0] == node:
				return (x[1],x[2])
			
	def decideIfArrived(self):
		pass
