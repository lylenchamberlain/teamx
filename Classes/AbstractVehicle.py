


class AbstractVehicle:
	
	def __init__(self,ID,v):
		self.ID = ID
		self.currentPossition=("Vertex",v)
		self.type=""
		self.capacity = 0
		
	def __str__(self):
		return str(self.ID)+ " at " + str(self.currentPossition[1])+" capacity "+str(self.capacity)+"tons type "+self.type
