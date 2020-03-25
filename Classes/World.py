from  Classes.AbstractWorld import AbstractWorld

import pygame
pygame.font.init() 

class World(AbstractWorld):
	
	def __init__(self):
		AbstractWorld.__init__(self)
		
		self.height = 600
		self.width = 800
		self.screen = pygame.display.set_mode((self.width, self.height))
		self.black = (0,0,0)
		self.clock = pygame.time.Clock()
		self.font  = pygame.font.SysFont('Comic Sans MS', 30)


	def runSimulation(self, fps=1, initialTime=5*60, finalTime=23*60):

		'''
		This will give you a list of ALL cars which are in the system
		'''
		trucks = self.getInitialTruckLocations()
		for i,t in enumerate(trucks):
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


			for x in range(len(self.Edges)):
				#Iterate through all the points of path
				for y in range(len(self.Edges[x][3]) - 1):
					pygame.draw.line(self.screen,(90,200,90), (self.Edges[x][3][y][0]*800, self.Edges[x][3][y][1]*800), (self.Edges[x][3][y+1][0]*800, self.Edges[x][3][y+1][1]*800) , 4)

					
			#Print out red rectangles for trucks just standing still
			#Initially this is where trucks are
			speed = [0,40]
			for x in trucks:
				
				for y in self.Verticies:
				# Find the index of the node position we care about
					
					if x.VehicleID == y[0]:
						x.currentVertex == y[0]
						pygame.draw.rect(self.screen,(255,0,0),(800*y[1],800*y[2],10,10))
			
			ogball = pygame.image.load("C:/Users/Lyle%20Chamberlain/eclipse-workspace/myTruck.png")
			ballRect = pygame.draw.rect(self.screen,(100,0,100),(500,500,40,40))
			#ballRect = ball.get_rect()
			ballRect = ballRect.move(speed)
			ballRect = ballRect.move(350,350)
			#self.screen.blit(ballRect)
					

			#We know the node that the truck is at
	
			
			'''
			You should plot the vetrices, edges and cars and customers
			Each time, cars will move and you should visualize it 
			accordingly
			'''
     
			pygame.display.update()	
			gameExit = False
			
			for event in pygame.event.get():
				
				if event.type == pygame.QUIT:
					gameExit = True
					pygame.quit()
					
				
				
			self.clock.tick(fps)
			if gameExit == True:
				break
