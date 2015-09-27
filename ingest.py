import csv
from dateutil import parser
import datetime
import collections
import pymongo

INFILE = './data/yellow_tripdata_2015-01.csv'

db = pymongo.MongoClient().taxi
db.trips.count()

print datetime.datetime.now()
for i, l in enumerate(csv.DictReader(open(INFILE))):
    if not(i%100000): print i
    date = parser.parse(l['tpep_pickup_datetime'])
    day = date.strftime('%A')
    time = int(date.strftime('%H')) * 60
    lat = round(float(l['pickup_longitude']), 3)
    lon = round(float(l['pickup_latitude']), 3)
    db.trips.update( {'time' : time, 'location' : (lat, lon)},
            {'$inc': {'count': 1 }}, upsert=True
    ) 
print datetime.datetime.now()
print len(out)
