#!/usr/bin/env python

"""Converts CSV with path/row center coordinates to MUX
scene boudaries geojson"""

import sys
import math
import geojson
from pyproj import Proj, transform
from shapely import geometry
from shapely.geometry import mapping
from shapely.affinity import rotate

def longitude_to_utm_epsg(longitude):
    """
    Return Proj4 EPSG for a given longitude in degrees
    """
    zone = int(math.floor((longitude + 180) / 6) + 1)
    epsg = '+init=EPSG:326%02d' % (zone)
    return epsg

def center_to_scene_boundaries(center_lat, center_lon,
                               previous_center_lat,
                               previous_center_lon):
    """
    Given a ll center coordinate generate a polygon geometry
    representing the scenes boundaries

    Input:
      center_lat, center_lon: scene center, degrees
      previous_center_lat, previous_center_lon: previous scene center,
        degrees
    """

    i_proj = Proj('+init=EPSG:4326')

    # Choose appropriate UTM projection for plain coordinates
    w_proj = Proj(longitude_to_utm_epsg(center_lon))
    
    center_ll = (center_lon, center_lat, 0)
    previous_center_ll = (previous_center_lon, previous_center_lat, 0)

    center_plain = transform(i_proj, w_proj, *center_ll)
    previous_center_plain = transform(i_proj, w_proj, *previous_center_ll)
    
    # Compute orbit inclination, which will be the
    # value used for image rotation
    rotation = math.degrees(math.atan((center_plain[1] -
                                       previous_center_plain[1])/
                                      (center_plain[0] -
                                       previous_center_plain[0])))

    #print center_plain
    # Half scene in meters
    hm = 20 * 2906

    plain = dict()
    plain['ul'] = (center_plain[0] - hm, center_plain[1] + hm, 0)
    plain['ur'] = (center_plain[0] + hm, center_plain[1] + hm, 0)
    plain['lr'] = (center_plain[0] + hm, center_plain[1] - hm, 0)
    plain['ll'] = (center_plain[0] - hm, center_plain[1] - hm, 0)
    #print plain

    # Generate and rotate plain polygon
    plain_pol = geometry.Polygon([plain['ul'][:2],plain['ur'][:2],plain['lr'][:2],plain['ll'][:2]])
    plain_pol = rotate(plain_pol, angle=rotation,
                       origin=center_plain[:2], use_radians=False)
    x, y = plain_pol.exterior.coords.xy
    
    # Plain to ll
    llc = dict()
    llc['ul'] = transform(w_proj, i_proj, x[0], y[0], 0)
    llc['ur'] = transform(w_proj, i_proj, x[1], y[1], 0)
    llc['lr'] = transform(w_proj, i_proj, x[2], y[2], 0)
    llc['ll'] = transform(w_proj, i_proj, x[3], y[3], 0)

    # Create output geometry
    pol = geometry.Polygon([llc['ul'][:2],llc['ur'][:2],llc['lr'][:2],llc['ll'][:2]])
   
    return pol
    
def csv_to_json(csv_file, start_row=1, end_row=400, start_path=1, end_path=373):
    """
    Dumps scene geojson from path/row information

    Input:
      start_row, end_row: only rows within this range are processed

    """

    features = []
    center_lat = None
    center_lon = None
    with open(csv_file, 'r') as fcsv:
        for line in fcsv:
            line = line[:-1]
            #print line
            fields = line.split(',')
            if fields[0] == 'PATH':
                # Header
                continue
            path = int(fields[0])
            row = int(fields[1])
            previous_center_lat = center_lat
            previous_center_lon = center_lon
            center_lat = float(fields[2])
            center_lon = float(fields[3])

            # Skip configured paths and rows
            if row < start_row or row > end_row:
                continue
            if path < start_path or path > end_path:
                continue
            #print fields

            pol = center_to_scene_boundaries(center_lat, center_lon,
                                             previous_center_lat,
                                             previous_center_lon)
            feature = geojson.Feature(geometry=pol,
                                      properties={"PATH":path, "ROW":row})
            features.append(feature)

    fc = geojson.FeatureCollection(features)
    print geojson.dumps(fc)

if __name__ == '__main__':
    """
    Given CSV of grid reference system dumps 
    geojson of MUX scenes to stdout.
    
    Scenes boundaries are approximate.

    Parameters:
      csv_input_filename: each line is path, row, lat, lon
    """
    assert len(sys.argv) == 2
    csv_to_json(sys.argv[1], start_row=5, end_row=199,
                start_path=1, end_path=373)
