from ResultsMailer import ResultsMailer

class TicketChecker:
	ballsMatching=0
	bonusMatching=False

	def __init__(self, draw, tickets):
		for ticket in tickets:
			self.ballsMatching=len(set(ticket.balls).intersection(draw.balls))
			self.bonusMatching=len(set(ticket.balls).intersection([draw.bonus]))!=0

			resultsMailer=ResultsMailer(draw,ticket,self)
