from AbstractVehicle import AbstractVehicle

class Vehicle(AbstractVehicle):
	
	def __init__(self,ID,v):
		AbstractVehicle.__init__(self,ID,v)
