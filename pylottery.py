#!/usr/bin/python3

from DrawRetriever import DrawRetriever

retriever = DrawRetriever()

draws = retriever.draws

for draw in draws:
	print(draw)
