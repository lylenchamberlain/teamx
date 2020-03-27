from Classes.World import AbstractWorld
from Classes.AbstractWorld import AbstractWorld
import pygame
import random

class Animation():
    #Use this for truck animations
    def determineStartNode(self):
        return 2
    
    def __init__(self, startingX, startingY,currentVertex):
        self.value = None
        self.speed = [0,0]
        self.speedX = 0
        self.speedY = 0
        self.currentNode = currentVertex
        self.startPointX = None
        self.startPointY = None
        self.ogball = pygame.image.load("myTrucky.png")
        self.ball = pygame.transform.scale(self.ogball,(19,19))
        self.ballrect = self.ball.get_rect()
        self.ballrect = self.ballrect.move(startingX, startingY)
        #self.startingFirstNode = 17
        randomValue = random.randrange( 100,400)
        self.truckList = []
        self.truckTop = self.ballrect.top
        self.truckLeft = self.ballrect.left
        self.nodeDestination = 0#NOde its supposed to end up at
        self.nodeFinalDestination = 0
        self.nodeDeparture = 0 # NOde it left from
        self.nextMoveTime = 0 # they should move every minutes
        self.currentPath = []   #Grab the truck wherever it is and go to start node
        self.status = 1 # 1 if moving to starting node, 2 if at starting node, #3 if moving to end node, 4 if done
        self.counter = 0
        self.currentPath2 = [] #Go from start to end node
        self.travelingPath = []

        
        

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
            
