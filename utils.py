import os
import gpxpy
import pandas as pd
import geopandas as gpd
from shapely.geometry import *

def saved_places(place):
    try:
        url = place['properties']['Google Maps URL']
    except KeyError:
        url = None
    try:
        business_name = place['properties']['Location']['Business Name']
    except KeyError:
        business_name = None
    try:
        title = place['properties']['Title']
    except KeyError:
        title = None
    try:
        address = place['properties']['Location']['Address']
    except KeyError:
        address = None
    try:
        lat = place['properties']['Location']['Geo Coordinates']['Latitude']
    except KeyError:
        lat = None
    try:
        lng = place['properties']['Location']['Geo Coordinates']['Longitude']
    except KeyError:
        lng = None
    try:
        country = place['properties']['Location']['Country Code']
    except KeyError:
        country = None        
    try:
        published = place['properties']['Published']
    except KeyError:
        published = None
    try:
        updated = place['properties']['Updated']
    except KeyError:
        updated = None
    try:
        geom_type = place['geometry']['type']
    except KeyError:
        geom_type = None
        
    if lat == None:
        try:
            lat = place['geometry']['coordinates'][1]
        except KeyError:
            lat = None
            
    if lng == None:
        try:
            lng = place['geometry']['coordinates'][0]
        except KeyError:
            lng = None        
        
    
    return {'Google_Maps_URL'.lower(): url,
            'Business_Name'.lower(): business_name,
            'Title'.lower(): title,
            'Address'.lower(): address,
            'Latitude'.lower(): lat,
            'Longitude'.lower(): lng,
            'country': country,
            'Published'.lower(): published,
            'Updated'.lower(): updated,
            'type'.lower(): geom_type}

# pprint(star['features'][2])
# saved_places(star['features'][1])

def between(a, lower, upper):
    assert lower <= upper
    if (a>=lower) and (a<=upper):
        return True
    else:
        return False
    
def gps(file):
    trail_name = file.split('/')[-1].split('.')[0]
    gpx_file = gpxpy.parse(open(file, 'r'))
    gpx_data = pd.DataFrame([{'latitude': _.latitude, 
                              'longitude': _.longitude, 
                              'elevation': _.elevation} for _ in gpx_file.routes[0].points])
    gpx_data['geometry'] = gpx_data.apply(lambda x: Point(x.longitude, x.latitude), axis=1)
    gpx_data['name'] = trail_name
    gpx_line = pd.DataFrame([{'geometry': LineString([[_.x, _.y] for _ in gpx_data.geometry]),
                              'name': trail_name}])
    return trail_name, gpx_data, gpx_line

def gps_folder(folder):
    points, lines = pd.DataFrame(), pd.DataFrame()
    files = os.listdir(folder)
    for file in files:
        # if file == 'Nymph, Dream, Haiyaha and Loch Vale Lakes Loop.gpx':
        #    continue
        abs_dir = folder + '/' + file
        trail_name, gpx_data, gpx_line = gps(abs_dir)
        print(trail_name)
        points = points.append(gpx_data)
        lines = lines.append(gpx_line)
    return points, lines