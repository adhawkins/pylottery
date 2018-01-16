import requests
import csv
from datetime import datetime
from LotteryDraw import LotteryDraw

class DrawRetriever:
	draws=[]

	def __init__(self):
		r = requests.get('https://www.national-lottery.co.uk/results/lotto/draw-history/csv')

		#print(r.text)

		CSVResults = csv.DictReader(r.text.splitlines())
		for CSVRow in CSVResults:
			draw=LotteryDraw(CSVRow['DrawNumber'],
					datetime.strptime(CSVRow['DrawDate'], '%d-%b-%Y').date(),
					sorted([ int(CSVRow['Ball 1']), int(CSVRow['Ball 2']), int(CSVRow['Ball 3']), int(CSVRow['Ball 4']), int(CSVRow['Ball 5']), int(CSVRow['Ball 6']) ]),
					int(CSVRow['Bonus Ball']),
				)

			self.draws.append(draw)

		self.draws = sorted(self.draws, key=lambda draw: draw.number)

