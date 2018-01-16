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
					sorted([ CSVRow['Ball 1'], CSVRow['Ball 2'], CSVRow['Ball 3'], CSVRow['Ball 4'], CSVRow['Ball 5'], CSVRow['Ball 6'] ], key=int),
					CSVRow['Bonus Ball'],
				)

			self.draws.append(draw)

		self.draws = sorted(self.draws, key=lambda draw: draw.number)

