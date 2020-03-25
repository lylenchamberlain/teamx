from Classes.AbstractVehicle import AbstractVehicle

class Vehicle(AbstractVehicle):
	
	def __init__(self,ID,v):
		self.VehicleID = ID
		self.currentVertex = v
		AbstractVehicle.__init__(self,ID,v)
