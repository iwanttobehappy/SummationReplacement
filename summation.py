import sys
import csv
import string
from datetime import date
from time import strptime
import datetime
import re
import argparse


filename=""
parser=argparse.ArgumentParser(description="Summations.py gives a list of summations that are ready for qc checks  ")
parser.add_argument('-f',action="store",dest="filename")

result=parser.parse_args()
filename=result.filename
#load up a csv in the following format CASE_NUMBER BODY_SITE PHYSICIAN_NAME REQUISITION_NUMBER DATE_RECEIVED DATE_REPORTED

rr=csv.reader(open(filename,'rb'),delimiter=',',quotechar='\'')
rr.next()

for r in rr:
	print r[4]