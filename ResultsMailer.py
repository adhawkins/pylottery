from subprocess import Popen, PIPE
from email.mime.text import MIMEText

class ResultsMailer:
	def __init__(self, draw, ticket, ticketChecker):
		body = "The numbers for draw " + draw.number + " (" + draw.date.strftime("%a %d %b %Y") + ") are:\n\n"
		for ball in draw.balls:
			body += str(ball) + " "

		body += "\nbonus " + str(draw.bonus) + "\n\n"

		body += "You matched " + str(ticketChecker.ballsMatching) + " "
		if ticketChecker.bonusMatching:
			body += "plus the bonus"

		body += "\n\n"

		subject=draw.date.strftime("%d/%m/%Y") + ": ";

		for ball in draw.balls:
			subject += str(ball) + " "

		subject+="(" + str(draw.bonus) + ") - " + str(ticketChecker.ballsMatching)

		if ticketChecker.bonusMatching:
			subject+="+B"

		#print("***")
		#print(body)
		#print(subject)

		p = Popen(["//usr/bin/Mail", "-s", subject, ticket.email], stdin=PIPE)
		p.communicate(bytearray(body, "ascii"))

