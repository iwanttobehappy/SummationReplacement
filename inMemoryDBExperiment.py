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
#load up a csv in the following format CASE_NUMBER BODY_SITE PHYSICIAN_NAME REQUISITION_NUMBER DATE_RECEIVED DATE_REPORTED PRACTICE
db = sqlite3.connect(':memory:')





def makePendingDays(dt):
	tmp=dt.split()
	t2=tmp[0].split("/")
	day=t2[1]
	month=t2[0]
	year=t2[2]
	
	dt=datetime.date(int(year),int(month),int(day))
	today=date.today()
	return abs((today-dt).days)



def lookupPractice(cgiId):
	global practice
	for key in practice:
		if key==cgiId:
			return simplifyPracticeName(practice[key])
	return "No Practice Associated"
		
def simplifyPracticeName(e):
	e=e.replace("NY Presbyterian Hosp. Weill Cornell Med. Ctr. MM Pgm.","Weill Cornell")
	e=e.replace("Chilton Memorial Hospital","Chilton")
	e=e.replace("Costa Rica","Roche")
	e=e.replace("Trinidad","Roche")
	e=e.replace("El Salvador","Roche")
	e=e.replace("Aruba","Roche")
	e=e.replace("Guatemala","Roche")
	e=e.replace("Panama","Roche")
	e=e.replace("Repbulic of Dominica","Roche")
	e=e.replace("Curacao","Roche")
	e=e.replace("Bahamas","Roche")
	e=e.replace("Jamaica","Roche")
	e=e.replace("Honduras","Roche")
	e=e.replace("University of Iowa HealthcareClinical Pathology Lab","UIowa")
	e=e.replace("Georgia Health Sciences University Medical Center","Georgia Health Sciences")
	e=e.replace("Research Long Island Jewish Medical Ctr.","LIJ")
	e=e.replace("Memorial Sloan-Kettering Cancer Center","MSKCC")
	e=e.replace("Regional Cancer Care Associates","Regional Cancer Care")
	e=e.replace("Weill Cornell Medical College","Weill Cornell")
	e=e.replace("Health Network Laboratories","HNL")
	e=e.replace("Republic Dominican","Roche")
	e=e.replace("Republic of Dominica","Roche")
	e=e.replace("Payson Pavilion","")
	return e

def init_db(cursor):
	cursor.execute('''CREATE TABLE cases(
			CaseNumber varchar,
			bodySite varchar,
			physicianName varchar,
			reqNumber varchar,
			dateReceived varchar,
			dateReported varchar,
			practice varchar)''')

def populate_db(cursor,csv_fp):
	rdr=csv.reader(csv_fp)
	cursor.executemany('''
		INSERT into cases (CaseNumber,bodySite,physicianName,reqNumber,dateReceived,dateReported,practice)
		VALUES (?,?,?,?,?,?,?)''', rdr)
		
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
practice=dict()
receiveDate=dict()
for i in cgiNumbers:
	sel="Select CaseNumber,dateReported,practice,dateReceived from cases where reqNumber='%s'" % i
	c.execute(sel)
	readyCases=list()

	for cn in c.fetchall():
		if cn[1]=="":
			readyCases.append(cn[0])
			practice[i]=cn[2]
			receiveDate[cn[0]]=cn[3]
	if len(readyCases)==1:
		if readyCases[0][0]=='X':
			print readyCases[0],i,lookupPractice(i),makePendingDays(receiveDate[readyCases[0]])
			
		
		
