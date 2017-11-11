from lxml import etree
from lxml import objectify
from geopy.distance import vincenty
from geopy import Point
import pandas
import json
from math import sqrt


class PathImporter:
    def __init__(self, path_file, stops_file):
        self.path = path_file
        self.stops = stops_file

    def run(self, output_file):
        '''output_file is a file like object'''
        # read path from gpx file's xml
        tree = etree.parse(self.path)
        root = tree.getroot()

        # read stops list
        stops = pandas.read_csv(self.stops, header=0)

        # convert xml to json
        points = [
            {
                'lat': float(pt.attrib['lat']),
                'lon': float(pt.attrib['lon']),
                'elevation': float(pt.find('{*}ele').text),
                '2d_dist': None,
                '3d_dist': None,
                'stop': None
            }
            for pt in root.findall('{*}trk/{*}trkseg/{*}trkpt')
        ]

        # calculate values between points on path
        for a,b in zip(points, points[1:] + points[0:1]):
            pt_a = Point(a['lat'], a['lon'])
            pt_b = Point(b['lat'], b['lon'])
            dist_2d = vincenty(pt_a, pt_b).meters
            dist_3d = sqrt(dist_2d**2 + (a['elevation'] - b['elevation'])**2)
            b['2d_dist'] = dist_2d
            b['3d_dist'] = dist_3d

        # find stops on path
        for i,(letter,lat,lon) in stops.iterrows():
            stop_pt = Point(lat,lon)
            dist = [ (i, vincenty(Point(x['lat'],x['lon']) ,stop_pt).meters)
                    for i,x in enumerate(points)]
            index,off_by = min(dist, key=lambda x: x[1])
            assert points[index]['stop'] is None
            points[index]['stop'] = letter
            # print(points[index]['stop'])
            # print(off_by)

        # write json
        json.dump(points, output_file, indent=4)

