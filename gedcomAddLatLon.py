#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This script reads a gedcom file and adds latitude
# and longitude to all places without these informations.
# The result is written in a new gedcom file.
#
# This script uses geopy to find the latitude and longitude
# of locations. You may have to install it with
# pip install geopy
#
# Since we can not perform too much requests, this script
# stores the result of the requests in a text file.

def addLatLon(gedcomFilename, outputFilename = None):
    cacheLatLonFilename ='citiesLatLon.txt'
    import os
    from geopy.geocoders import Nominatim
    getLatStr = lambda lat: ('N' if lat>0 else 'S') + str(abs(lat))
    getLonStr = lambda lon: ('E' if lon>0 else 'W') + str(abs(lon))

    def loadCitiesLatLon(filename = cacheLatLonFilename):
        if not os.path.exists(filename): return {}
        lines = [c.strip() for c in open(filename,'r', encoding='utf-8').readlines()]
        data=[lines[i-1] + ':' + lines[i][1:-1] for i in range(len(lines)) if lines[i].startswith('(')]
        d={}
        for line in data:
            city, latlon = line.split(':')
            lat,lon = latlon.split(',')
            key = city.strip()
            d[key] = (float(lat),float(lon))
        return d

    def saveCitiesLatLon(citiesLatLon, filename = cacheLatLonFilename):
        f = open(filename,'w')
        for city in sorted(citiesLatLon.keys()):
            f.write(city+'\n')
            f.write('('+str(citiesLatLon[city][0])+','+str(citiesLatLon[city][1])+')\n')
        f.close()
    cities = loadCitiesLatLon(filename = cacheLatLonFilename)
    geolocator = Nominatim()
    lines = [c.strip() for c in open(gedcomFilename, 'r', encoding='utf-8').readlines()]
    newLines = []
    for i, line in enumerate(lines):
        newLines.append(line)
        if line.startswith('2 PLAC') and not lines[i+1].startswith('3 MAP'): 
            address = line.split('PLAC')[1].strip()
            if address.split(',')[0].strip()=='?': continue
            if address in cities:
                newLines.append('3 MAP')
                newLines.append('4 LATI ' + getLatStr(cities[address][0]))
                newLines.append('4 LONG ' + getLonStr(cities[address][1]))            
            else:
                try:
                    location = geolocator.geocode(address)
                    if location:
                        cities[address]=(location.latitude, location.longitude)
                        print(address)
                        print((location.latitude, location.longitude))
                        newLines.append('3 MAP')
                        newLines.append('4 LATI ' + getLatStr(location.latitude))
                        newLines.append('4 LONG ' + getLonStr(location.longitude))
                    else:
                        location = geolocator.geocode(address.split(',')[0])
                        if location:
                            print(address)
                            cities[address]=(location.latitude, location.longitude)
                            print((location.latitude, location.longitude))
                            newLines.append('3 MAP')
                            newLines.append('4 LATI ' + getLatStr(location.latitude))
                            newLines.append('4 LONG ' + getLonStr(location.longitude))
                except:
                    print('Can not get lat/lon for ' + address)
    saveCitiesLatLon(cities, filename = cacheLatLonFilename)
    if outputFilename is None:
        outputFilename = os.path.splitext(gedcomFilename)[0]+'_WithLatLon.ged'
    open(outputFilename, 'w').writelines('\n'.join(newLines))

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
        description = 'This script adds latitude/longitude to a gedcom file')
    parser.add_argument('-g','--gedcom', type = str, default = 'my_gedcom_file.ged',
                       help = 'Gedcom filename')
    parser.add_argument('-o','--outputGedcom', type = str, default = None,
                       help='Optional output name. If not provided, a filename will be generated from the gedcom filename')
    args = parser.parse_args()
    addLatLon(gedcomFilename = args.gedcom, outputFilename = args.outputGedcom)
