#!/usr/bin/python3

from DrawRetriever import DrawRetriever
from DrawRetriever2 import DrawRetriever2
from PyLotteryDB import PyLotteryDB
from TicketChecker import TicketChecker

retriever = DrawRetriever2()
draws = retriever.draws

DB = PyLotteryDB()
tickets = DB.retrieveTickets()

for draw in draws:
	if not DB.drawExists(draw.number):
		checker=TicketChecker(draw,tickets)
		DB.recordDraw(draw)

