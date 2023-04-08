#!/usr/bin/env python3

"""Concatenate prec from the MERRA2
reanalysis."""

import iris
import numpy as np
import matplotlib as mpl
from iris.util import unify_time_units
from iris.util import equalise_attributes
from iris.analysis import MEAN
import iris.coord_categorisation

def clean_callback(cube,field,filename):
    cube.coord('time').attributes = {}

# read prec file.
pr_file = '/Volumes/climate_lab2/MERRA2/Daily_and_Subdaily/Precipitation_biascorrected_daily/MERRA2.tavg1_2d_flx_Nx.20200101.SUB.nc'

pr = iris.load_cube(pr_file, 'total_precipitation', callback=clean_callback)

my_coord = pr.coord("time")
my_coord.points = my_coord.points.astype(np.float64)

#time mean
iris.coord_categorisation.add_day_of_year(pr,'time',name='day_of_year')
pr = pr.aggregated_by(['day_of_year'], iris.analysis.MEAN)

dd = np.arange('2020-01-02', '2021-01-01', dtype='datetime64')

dd = np.datetime_as_string(dd)

hyphenlist = dd
newlist = []

for x in hyphenlist:
    newlist.append(x.replace('-', ''))

dd = newlist

for i in dd:
    print(i)
    # read prec file.
    pr_file = '/Volumes/climate_lab2/MERRA2/Daily_and_Subdaily/Precipitation_biascorrected_daily/MERRA2.tavg1_2d_flx_Nx.'+str(i)+'.SUB.nc'
    pr_n = iris.load_cube(pr_file, 'total_precipitation', callback=clean_callback)
    
    my_coord = pr_n.coord("time")
    my_coord.points = my_coord.points.astype(np.float64)
    
    #time mean
    iris.coord_categorisation.add_day_of_year(pr_n,'time',name='day_of_year')
    pr_n = pr_n.aggregated_by(['day_of_year'], iris.analysis.MEAN)

    cube = iris.cube.CubeList([pr,pr_n])
    iris.util.unify_time_units(cube)
    equalise_attributes(cube)
    pr = cube.concatenate_cube()

iris.save(pr,'/Users/lais3/Desktop/prec_conc/MERRA2.tavg1_2d_flx_Nx.2020.SUB.nc')


