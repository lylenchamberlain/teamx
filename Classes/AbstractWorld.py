

from Classes.Vehicle import Vehicle
from Classes.Order import Order

import numpy as np
import pickle
class AbstractWorld:
	
	def __init__(self):
		
		[VF,EF] = pickle.load(open("./Classes/data/Lehigh.pickle",'rb'),encoding = "Latin1")
		#with open("old_pickle.pkl", 'rb') as f:
    	#loaded = pickle.load(f, encoding="latin1") 
		
		self.Edges=[] 
		for edge in EF:
			self.Edges.append( [ edge[0] , edge[1] ,EF[edge][0 ],EF[edge][1 ],EF[edge][2 ] ])	
			#print("First Value", edge[0], "Second Value", edge[1], "Third Value", EF[edge][0])		
 
		
		self.Verticies=[]
		for v in VF:
			self.Verticies.append(  [ v,float(VF[v][0]),float(VF[v][1])]  )	
			#print("v ", v, "float(VF[v][0])", float(VF[v][0])	, " last value ", float(VF[v][1]))
		 
		
		self.v = [v[0] for v in self.Verticies]
		self.orderId = 0
		
	def getInitialTruckLocations(self):
		np.random.seed(47)
		vehicles = []
		np.random.shuffle(self.v)
	
		for i, v in enumerate(self.v):
			if i%3 == 0:
				newVehicle = Vehicle(i,v)
				newVehicle.type="Truck"
				newVehicle.capacity = np.random.randint(3,30)
				vehicles.append(newVehicle)
		return vehicles
		
	def getNewOrdersForGivenTime(self,t):
		newOrders=[]
		np.random.seed(t)
		if t > 22*60:
			return newOrders
		if np.random.rand() < 0.3:
			n = np.random.randint(1,3)
			np.random.shuffle(self.v)
			for j in range(n):
				order = Order(self.orderId)
				self.orderId+=1
				newOrders.append(order)
		return newOrders
		 


