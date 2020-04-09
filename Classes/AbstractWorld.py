from Classes.Vehicle import Vehicle
from Classes.Order import Order

import numpy as np
import pickle
class AbstractWorld:
	
	def __init__(self):
		
		[VF,EF] = pickle.load(open("./Classes/data/Lehigh.pickle",'rb'), encoding = "Latin1")
		self.Edges=[] 
		for edge in EF:
			self.Edges.append( [ edge[0] , edge[1] ,EF[edge][0 ],EF[edge][1 ],EF[edge][2 ] ])			
 
		
		self.Verticies=[]
		for v in VF:
			self.Verticies.append(  [ v,float(VF[v][0]),float(VF[v][1])]  )			
		 
		
		self.v = [v[0] for v in self.Verticies]
		
		self.vShuffled=[v[0] for v in self.Verticies]
		np.random.seed(47)
		np.random.shuffle(self.vShuffled)
		
		self.orderId = 0
		self.map = {"L1":["A","B"],"L2":["C","D"],"L3":["E","F"],"L4":["G","H"]}
		self.getProductionLines()
		

		
		
	def getLocationOfWarehouses(self):	
		types = ["A","B","C","D","E","F","G","H"]
		Warehouses = []
		j = 0
		for t in types:
			for k in range(2):
				Warehouses.append({"type":t,"location":self.vShuffled[j]})
				j+=1
		return Warehouses
		
	def getProductionLines(self):	
		types = ["L1","L2","L3","L4"]
		ProductionLines = []
		j = 20
		for t in types:
			for k in range(5):
				ProductionLines.append({
				"type":t,
				"location":self.vShuffled[j],
				"capacityOfMaterial[tons]":100})
				j+=1
		print("self.vshuffle", ProductionLines)
		return ProductionLines
		
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
				order.finalLocation=np.random.choice(self.vShuffled[40:])
				
				l = [e for e in self.map]
				np.random.shuffle(l)

				for j in l[0:np.random.randint(2,4)]:
					order.productionProcess.append({
						"processinLine":j,
						"resourceNeeded":np.random.choice(self.map[j]),
						"processingTime":np.random.randint(5,10),
						"materialNeeded[tons]":np.random.randint(2,10),						
						})
				
				
				 
				self.orderId+=1
				newOrders.append(order)
		return newOrders
		 


