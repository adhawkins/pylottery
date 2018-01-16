class LotteryTicket:
	email=""
	balls=[]

	def __init__(self,email,balls):
		self.email=email
		self.balls=balls

	def __str__(self):
		return "Email: " + self.email + ", balls: '" + " ".join(map(str,self.balls)) + "'"
