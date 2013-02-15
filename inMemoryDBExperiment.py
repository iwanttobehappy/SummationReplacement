import sys
import csv
import sqlite3
import string
from datetime import date
from time import strptime
import datetime
import re
import argparse

#read in csv file and create an in memory db

filename=""
parser=argparse.ArgumentParser(description="Summations.py gives a list of summations that are ready for qc checks  ")
parser.add_argument('-f',action="store",dest="filename")

result=parser.parse_args()
filename=result.filename
#load up a csv in the following format CASE_NUMBER BODY_SITE PHYSICIAN_NAME REQUISITION_NUMBER DATE_RECEIVED DATE_REPORTED
db = sqlite3.connect(':memory:')

def init_db(cursor):
	cursor.execute('''CREATE TABLE cases(
			CaseNumber varchar,
			bodySite varchar,
			physicianName varchar,
			reqNumber varchar,
			dateReceived varchar,
			dateReported varchar)''')

def populate_db(cursor,csv_fp):
	rdr=csv.reader(csv_fp)
	cursor.executemany('''
		INSERT into cases (CaseNumber,bodySite,physicianName,reqNumber,dateReceived,dateReported)
		VALUES (?,?,?,?,?,?)''', rdr)
		
c=db.cursor()
init_db(c)
populate_db(c,open(filename))
db.commit()

c.execute("Select CaseNumber,reqNumber from cases order by reqNumber")

cgiNumbers=set()

for i in c.fetchall():
	cgiNumbers.add(i[1])
	#print i[0],i[1]
	
#now I have a list of cgi numbers now let's get the cases

for i in cgiNumbers:
	sel="Select CaseNumber,dateReported from cases where reqNumber='%s'" % i
	c.execute(sel)
	for cn in c.fetchall():
		if cn[1]=="":
			print cn[0],i

