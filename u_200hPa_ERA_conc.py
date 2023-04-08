#!/usr/bin/env python3

"""Concatenate u-wind from the ERA
reanalysis at 200 hPa."""

import iris
import numpy as np
import matplotlib as mpl
from iris.util import unify_time_units
from iris.util import equalise_attributes

def clean_callback(cube,field,filename):
    cube.coord('t').attributes = {}

# read u_wind file.
u_file = '/Volumes/Elements/nc_files/ERA-INTERIM/U200/U.1979.global_domain.nc'

# constraining between +/- 36 latitude.
lat_35 = iris.Constraint(latitude=lambda v: -36 <= v <= 36)
u = iris.load_cube(u_file, lat_35, callback=clean_callback)

# verifying the new lat.
lat = u.coord('latitude')
lat = lat.points

yy = np.arange(1980,2010,1,dtype=int)
yy = list(yy)

for i in yy:
    print(i)
    # read STRF file.
    u_file = '/Volumes/Elements/nc_files/ERA-INTERIM/U200/U.'+str(i)+'.global_domain.nc'
    # constraining between +/- 36 latitude.
    lat_35 = iris.Constraint(latitude=lambda v: -36 <= v <= 36)
    u_n = iris.load_cube(u_file,lat_35, callback=clean_callback)

    cube = iris.cube.CubeList([u,u_n])
    iris.util.unify_time_units(cube)
    equalise_attributes(cube)
    u = cube.concatenate_cube()

iris.save(u,'/Volumes/Elements/nc_files/ERA-INTERIM/U200/ERA.jan-dec_dmeans_ts.1979-2009.u200.nc')


