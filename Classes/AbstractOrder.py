


class AbstractOrder:
	
	
	
	def __init__(self, id):
		self.id = id
		self.finalLocation=None
		self.productionProcess=[]
		
		
		
	def __str__(self):
		return "Order %d "% (self.id)
