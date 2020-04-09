from Classes.World import AbstractWorld
from Classes.AbstractWorld import AbstractWorld
import pygame
import random

#Stores facts about our trucks
class Animation():

    
    def __init__(self, currentVertex, capacity):
        #This is the node the truck is currently out
        self.currentNode = currentVertex
        
        #The following creates a rectangle and  image for the truck
        self.ogball = pygame.image.load("myTrucky.png")
        self.ball = pygame.transform.scale(self.ogball,(25,25))
        self.ballrect = self.ball.get_rect()


        self.status = 4 # 1 if moving to starting node, 2 if at starting node, #3 if moving to end node, 4 if done
        #This counter is used to figure out what point on the path the truck is at
        self.bigCounter = 0
        self.smallCounter = 0
        self.finalNode = 1000
        self.processTimes = []

        self.currentLoad = "" #String of the job its carrying
        self.thirdListEasy = []
        self.truckPath = []
        self.timeNeeded = []
        self.dict = {}
        self.capacity = capacity


        
    '''***This does nothing but might be helpful for new animation***
    def determineSpeed(self, firstNode, secondNode):
        firstNodeCoordinates = Animation.nodeToCoordinate(self,firstNode)
        secondNodeCoordinates = Animation.nodeToCoordinates(self,secondNode)
        newSpeed = secondNodeCoordinates - firstNodeCoordinates
        self.speed = newSpeed
     '''
        