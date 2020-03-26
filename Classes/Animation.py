from Classes.World import AbstractWorld

class Animation:
    #Use this for truck animations
   
    def _init_(self):
        '''#Creates trucks
        self.speed = [0,0]
        print("GOGO")
        self.ogball = pygame.image.load("myTrucky.png")
        self.ball = pygame.transform.scale(self.ogball,(30,30))
        self.ballrect = self.ball.get_rect()
        self.ballrect = self.ballrect.move(350,350)
        self.truckList = []
        '''
        self.value = 3
        
    
    def generatesRandomVerticies(self):
        print("generateIt")
        return 2
        
    def generateTrucklist(self, trucks):
        
        x = 0
        
        for i in trucks:
            print("I", i)
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
            
        
    
        