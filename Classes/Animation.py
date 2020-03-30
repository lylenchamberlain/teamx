from Classes.World import AbstractWorld
from Classes.AbstractWorld import AbstractWorld
import pygame
import random

#Stores facts about our trucks
class Animation():

    
    def __init__(self, currentVertex):

        #speed in x and y directions
        self.speedX = 0
        self.speedY = 0
        #This is the node the truck is currently out
        self.currentNode = currentVertex
        
        #The following creates a rectangle and  image for the truck
        self.ogball = pygame.image.load("myTrucky.png")
        self.ball = pygame.transform.scale(self.ogball,(25,25))
        self.ballrect = self.ball.get_rect()

        self.nodeDestination = 0#NOde its supposed to end up at
        self.nodeFinalDestination = 0
        self.nodeDeparture = 0 # Node it left from
        self.nextMoveTime = 0 # they should move every minutes
        self.currentPath = []   #Grab the truck wherever it is and go to start node
        self.currentPath2 = [] #Go from start to end node

        self.status = 4 # 1 if moving to starting node, 2 if at starting node, #3 if moving to end node, 4 if done
        #This counter is used to figure out what point on the path the truck is at
        self.counter = 0

        self.currentLoad = "" #String of the job its carrying
        self.thirdListEasy = []


        
    '''***This does nothing but might be helpful for new animation***
    def determineSpeed(self, firstNode, secondNode):
        firstNodeCoordinates = Animation.nodeToCoordinate(self,firstNode)
        secondNodeCoordinates = Animation.nodeToCoordinates(self,secondNode)
        newSpeed = secondNodeCoordinates - firstNodeCoordinates
        self.speed = newSpeed
     '''
        