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
			for c in newOrders:
				print(c)
			
			text = self.font.render("Time: %02d:%02d"%(t/60, t%60), True, (255, 0, 0), (255, 255, 255))
			textrect = text.get_rect()
			textrect.centerx = 100
			textrect.centery = 30
			self.screen.fill((255, 255, 255))
			self.screen.blit(text, textrect)
 			

			#print Vertices
			for item in range(len(self.Verticies)):
				pygame.draw.rect(self.screen,(0,0,0),(800*self.Verticies[item][1],800*self.Verticies[item][2],10,10))
				print(self.Verticies[item])


			#l = [item for n]
			
			
			#Printing the edges
			for x in range(len(self.Edges)):
				

				
				#The first two values in the list given in 'Edges' are the integer values of the two nodes that the line connects
				#The following lines identify the integer value that identifies the node to connect
				firstNode = self.Edges[x][0]
				secondNode = self.Edges[x][1]
				
				#These variables will store the index in Vertices that holds the value we care about
				firstIndex = 0
				secondIndex = 0
				
				#The Highest unique node value is 229 but the Vertice list length is 189
				#THIS MEANS THAT THEY SKIPPED NUMBERS WHEN IDENTIFYING THE NODES AND IT DOESN'T CONTAIN ALL VALUES (0-229)
				#We need to find the index value we care about (for example node 289 happens to be at index 189)
				
				for x in range(len(self.Verticies)):
					#If the unique verticy number (the first value in the list) is the value we want (identified from above)
					#then we want to store the index that particular node is at. 
					if self.Verticies[x][0] == firstNode:
						firstIndex = x 
						break
				#This is the same as above but we're finding the index within Verticies for the second node value
				for y in range(len(self.Verticies)):
					if self.Verticies[y][0] == secondNode:
						secondIndex = y
						break
						
				
				
				''' The following are just testing print statements
				print("x value", x)
				print("first node value ",  self.Verticies[firstIndex][1])
				print('First part two ', self.Verticies[firstIndex][2])
				print(self.Verticies[220])
				print("Second Node ", secondNode)
				print("Verticie Length", len(self.Verticies))
				print(self.Verticies[188])
				print(self.Verticies)
				print('Second vertcie ', self.Verticies[secondNode][0])
				print("First thing ", firstNode, "Second Think ", self.Verticies[firstNode][1])
				'''
				#Draw the line
				#line(surface, color, start_pos, end_pos, width) 
				#Surface and color are easy
				#Start position is given by the x and y coordinate of the first node. 
				#Because we know the index value of the node we care about from above, we use that to search the list of Verticies
				#We do this for the x and y values (lovated at 1 and 2)
				# We then do the same for the second node

				
				pygame.draw.line(self.screen,(90,200,90), (self.Verticies[firstIndex][1]*800,self.Verticies[firstIndex][2]*800), (800* self.Verticies[secondIndex][1], 800* self.Verticies[secondIndex][2]), 4)
			

			
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
