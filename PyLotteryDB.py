import sqlite3
from LotteryDraw import LotteryDraw
from LotteryTicket import LotteryTicket
import os.path

class PyLotteryDB:
	def __init__(self):
		self.conn = sqlite3.connect(os.path.join(os.path.dirname(os.path.realpath(__file__)),'pylottery.sqlite'))
		self.conn.row_factory = sqlite3.Row
		self.checkTables()

	def checkTables(self):
		if not self.tableExists('draws'):
			self.createDrawsTable()

		if not self.tableExists('tickets'):
			self.createTicketsTable()

	def tableExists(self,table):
		cursor=self.conn.execute("SELECT count(name) from sqlite_master where type='table' and name=?", [table])
		return(cursor.fetchone()[0]!=0)

	def createDrawsTable(self):
		self.conn.execute('''CREATE TABLE draws(draw INTEGER PRIMARY KEY,
								date DATE,
								num1 INTEGER,
								num2 INTEGER,
								num3 INTEGER,
								num4 INTEGER,
								num5 INTEGER,
								num6 INTEGER,
								bonus INTEGER)''')

	def createTicketsTable(self):
		self.conn.execute('''CREATE TABLE tickets(email TEXT PRIMARY KEY,
								num1 INTEGER,
								num2 INTEGER,
								num3 INTEGER,
								num4 INTEGER,
								num5 INTEGER,
								num6 INTEGER)''')

	def drawExists(self,draw):
		cursor=self.conn.execute("SELECT count(draw) from draws where draw=?", [draw])
		return(cursor.fetchone()[0]!=0)

	def recordDraw(self,draw):
		cursor=self.conn.execute("INSERT into draws values(?,?,?,?,?,?,?,?,?)",
				[
					draw.number,
					draw.date,
					draw.balls[0],
					draw.balls[1],
					draw.balls[2],
					draw.balls[3],
					draw.balls[4],
					draw.balls[5],
					draw.bonus,
				]
			)
		self.conn.commit()

	def retrieveTickets(self):
		tickets=[]
		cursor=self.conn.execute("SELECT * from tickets")
		for row in cursor:
			tickets.append(LotteryTicket(
						row['email'],
						[ row['num1'], row['num2'], row['num3'], row['num4'], row['num5'], row['num6'] ]
					)
				)

		return tickets
