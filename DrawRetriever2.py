import requests
import csv
from datetime import datetime
from LotteryDraw import LotteryDraw
from bs4 import BeautifulSoup

class DrawRetriever2:
	draws=[]

	def __init__(self):
		r = requests.get('http://lottery.merseyworld.com/cgi-bin/lottery?days=2&Machine=Z&Ballset=0&order=1&show=1&year=-1&display=CSV')

		#print(r.text)

		bsObj = BeautifulSoup(r.text, "lxml")
		#print(bsObj.pre.string)

		lines=bsObj.pre.string.splitlines()
		lines.pop(0)
		lines.pop(0)

		CSVResults = csv.DictReader(lines)
		for CSVRow in CSVResults:
			if CSVRow['DD']:
				dateString=CSVRow['DD']
				dateString+="-"
				dateString+=CSVRow['MMM']
				dateString+="-"
				dateString+=CSVRow['YYYY']

				draw=LotteryDraw(CSVRow['No.'],
						datetime.strptime(dateString, '%d-%b-%Y').date(),
						sorted([ int(CSVRow[' N1']), int(CSVRow['N2']), int(CSVRow['N3']), int(CSVRow['N4']), int(CSVRow['N5']), int(CSVRow['N6']) ]),
						int(CSVRow['BN']),
					)

				self.draws.append(draw)

		self.draws = sorted(self.draws, key=lambda draw: draw.number)

