from Classes.World import AbstractWorld
from Classes.AbstractWorld import AbstractWorld
import pygame
import random

class Animation():
    #Use this for truck animations
    def determineStartNode(self):
        return 2
    
    def __init__(self):
        self.value = None
        self.speed = [0,0]
        self.ogball = pygame.image.load("myTrucky.png")
        self.ball = pygame.transform.scale(self.ogball,(19,19))
        self.ballrect = self.ball.get_rect()
        self.startingFirstNode = 17
        randomValue = random.randrange( 100,400)
        self.ballrect = self.ballrect.move(randomValue,randomValue)
        self.truckList = []
        self.speedX = 0
        self.speedY = 0
        self.startPointX = 0
        self.startPointY = 0
        
        

    def myInit(self):

        self.value = 5
        print("STARTED INIT ")
        
    
    def generatesRandomVerticies(self):
        print("generateIt")
        #self.value = 2
        #return self.value
        
    def generateTrucklist(self, trucks):
        
        x = 0
        
        for i in trucks:
            myAnimate = Animation()
            truckList.append(myAnimate)
            
            truckList[x].currentNodePosition = i.currentVertex
            
            
        x+=1    
        
        return truckList
    
    def determineSpeed(self, firstNode, secondNode):
        firstNodeCoordinates = Animation.nodeToCoordinate(self,firstNode)
        secondNodeCoordinates = Animation.nodeToCoordinates(self,secondNode)
        newSpeed = secondNodeCoordinates - firstNodeCoordinates
        self.speed = newSpeed
        
        
    
    def nodeToCoordinate(self, node):
        print("HUH")
        for x in myWorld.verticies:
            if myWorld.verticies[x][0] == node:
                return (myWorld.verticies[x][1], myWorld.verticies[x][2])
            
