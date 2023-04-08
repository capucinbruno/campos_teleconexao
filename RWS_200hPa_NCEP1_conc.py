#!/usr/bin/env python3

"""Concatenate RWS from the NCEP1
reanalysis (wind at 200 hPa)."""

import iris
import numpy as np
import matplotlib as mpl
from iris.util import unify_time_units
from iris.experimental.equalise_cubes import equalise_attributes

def clean_callback(cube,field,filename):
    cube.coord('time').attributes = {}

# read vp file.
S_file = '/media/oem/Elements/nc_files/NCEP1/RWS/RWS_200hPa_1979.nc'

# constraining between +/- 75 latitude.
lat_75 = iris.Constraint(latitude=lambda v: -76 <= v <= 76)
S = iris.load_cube(S_file, lat_75, callback=clean_callback)

# verifying the new lat.
#lat = vp.coord('latitude')
#lat = lat.points

yy = np.arange(1980,2010,1,dtype=int)
yy = list(yy)

for i in yy:
    print(i)
    # read STRF file.
    S_file = '/media/oem/Elements/nc_files/NCEP1/RWS/RWS_200hPa_'+str(i)+'.nc'
    # constraining between +/- 75 latitude.
    lat_75 = iris.Constraint(latitude=lambda v: -76 <= v <= 76)
    S_n = iris.load_cube(S_file,lat_75, callback=clean_callback)

    cube = iris.cube.CubeList([S,S_n])
    iris.util.unify_time_units(cube)
    equalise_attributes(cube)
    S = cube.concatenate_cube()

iris.save(S,'/media/oem/Elements/nc_files/NCEP1/RWS/NCEP1.jan-dec_dmeans_ts.1979-2009.RWS200.nc')












