import pymongo
import datetime
import time
from flask import Flask, render_template, g, request
import json

NYC_POINTS = (74.258 - 73.700) * 1000 * (40.917 - 40.477) * 1000

app = Flask(__name__)
app.config.from_object(__name__)


def connect_db():
    db = pymongo.MongoClient().taxi
    return db

connect_db().trips.create_index([('location', pymongo.GEO2D)])


def get_better(time=None, lat=-74.00594, lon=40.71278):
    if isinstance(lat, list): lat = float(lat[0])
    if isinstance(lon, list): lon = float(lon[0])
    location = (lon, lat)
    time = time or datetime.datetime.now()
    time = int(time.strftime('%H')) * 60
    near = g.db.trips.aggregate([
        {'$geoNear': {
            'near': location,
            'query': {'time': time},
            'distanceField': 'distance',
            'limit': 20
        }
        },
        {'$sort': {
            'count': -1
        }
        }
    ])
    percent_loaded = float(g.db.trips.count()) / 12748987
    return [{
        'location': i['location'],
        'distance': i['distance'],
        'hour': float(i['time']) / 60,
        'avg': round((float(i['count']) / (24 * 31)) / percent_loaded, 2)
    }
        for i in near]


def get_prediction(time=None, lat=-74.00594, lon=40.71278):
    if isinstance(lat, list): lat = float(lat[0])
    if isinstance(lon, list): lon = float(lon[0])
    location = (lon, lat)
    time = time or datetime.datetime.now()
    time = int(time.strftime('%H')) * 60
    near = g.db.trips.find(
        {
            'location': {'$near': location},
            'time': time
        }
    ).limit(1)
    percent_loaded = float(g.db.trips.count()) / 12748987
    return [{
        'location': i['location'],
        'hour': float(i['time']) / 60,
        'avg': round((float(i['count']) / (24 * 31)) / percent_loaded, 2)
    }
        for i in near]


@app.before_request
def before_request():
    g.db = connect_db()


@app.route('/')
def show_entries():
    return render_template('main.html')


@app.route('/api/prediction')
def prediction():
    result = get_prediction(**request.args)
    return json.dumps(result)


@app.route('/api/better')
def better():
    result = get_better(**request.args)
    return json.dumps(result)


if __name__ == '__main__':
    app.run(debug=True)
    # print location
    # print get_prediction()[0], get_better()[0]
    # print get_near(time=datetime.datetime.now() + datetime.timedelta(hours=6))[0]
    # print get_near(location=(-73.9935,40.75057))[0]
    # print get_near(location=(-73.99717, 40.73695))[0]
