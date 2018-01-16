from datetime import date

class LotteryDraw:

	number=-1
	date=date.today()
	balls=[]
	bonus=-1

	def __init__(self, number, date, balls, bonus):
		self.number = number
		self.date = date
		self.balls = balls
		self.bonus = bonus

	def __str__(self):
		return "Num: " + self.number + ", date: " + self.date.isoformat() + ", balls: '" + " ".join(map(str,self.balls)) + "', bonus: " + str(self.bonus)
