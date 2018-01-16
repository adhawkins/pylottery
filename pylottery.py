#!/usr/bin/python3

from DrawRetriever import DrawRetriever
from PyLotteryDB import PyLotteryDB

retriever = DrawRetriever()

draws = retriever.draws

#for draw in draws:
#	print(draw)

DB = PyLotteryDB()

#for draw in draws:
#	if not DB.drawExists(draw.number):
#		DB.recordDraw(draw)

tickets = DB.retrieveTickets()
for ticket in tickets:
	print(ticket)
