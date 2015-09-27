import pymongo
import csv
import datetime


INFILE = './data/sample.csv'
print datetime.datetime.now()
db.trips.insert_many([i for i in csv.DictReader(open(INFILE))])
db.trips.count()
print datetime.datetime.now()
