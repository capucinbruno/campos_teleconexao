#!/usr/bin/env python3

""" 9. Merge and Concatenate 
Examples from http://scitools.org.uk/iris/docs/latest/userguide """

# 9.1 Merge
# 9.1.1. Using CubeList.merge

# 9.2 Concatenate
import iris  
from iris.util import unify_time_units
import numpy as np

fname = '/media/oem/Elements/nc_files/NCEP_data/wind_200hPa/uwnd/uwnd.1979.nc'
u79 = iris.load_cube(fname)

fname = '/media/oem/Elements/nc_files/NCEP_data/wind_200hPa/uwnd/uwnd.1980.nc'
u80 = iris.load_cube(fname)

fname = '/media/oem/Elements/nc_files/NCEP_data/wind_200hPa/uwnd/uwnd.1981.nc'
u81 = iris.load_cube(fname)

cubes = iris.cube.CubeList([u79, u81])

print(cubes[0].coord('time').units)
print(cubes[1].coord('time').units)

print(cubes[0].coord('time').dtype)
print(cubes[1].coord('time').dtype)

print(cubes[0].coord('time'))
print(repr(cubes[1].coord('time')))

iris.util.unify_time_units(cubes)

new_cube = cubes.concatenate_cube()











