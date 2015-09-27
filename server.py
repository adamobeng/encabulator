import pymongo
import datetime
import time

NYC_POINTS = (74.258 - 73.700) * 1000 * (40.917 - 40.477) * 1000

db = pymongo.MongoClient().taxi
db.trips.create_index([('location', pymongo.GEO2D)])

def get_better(time =datetime.datetime.now() ,location =  (-74.00594, 40.71278)):
    time = int(time.strftime('%H')) * 60
    near = db.trips.aggregate([
        {'$geoNear': {
            'near': location,
            'query' : {'time' : time},
            'distanceField' : 'distance',
            'limit': 100
            }
        },
        {'$sort': {
            'count': -1
           }
        }
    ])
    percent_loaded = float(db.trips.count())/12748987
    return [{
        'location': i['location'],
        'distance': i['distance'],
        'hour' : float(i['time'])/60,
        'time': i['time'],
        'avg': (float(i['count'])/(24*31))/percent_loaded
        }
        for i in near]

def get_prediction(time =datetime.datetime.now() ,location =  (-74.00594, 40.71278)):
    time = int(time.strftime('%H')) * 60
    near = db.trips.find(
            {
            'location': {'$near': location},
            'time' : time
            }
    ).limit(1)
    return [{
        'location': i['location'],
        'hour' : float(i['time'])/60,
        'time': i['time'],
        'avg': (float(i['count'])/(24*31))/percent_loaded
        }
        for i in near]


print location
print get_prediction()[0], get_near()[0]

print get_near(time=datetime.datetime.now() + datetime.timedelta(hours=6))[0]
print get_near(location=(-73.9935,40.75057))[0]


print get_near(location=(-73.99717, 40.73695))[0]

