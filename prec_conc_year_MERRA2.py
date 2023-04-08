#!/usr/bin/env python3

"""Concatenate prec from the MERRA2
reanalysis by year"""

import iris
import numpy as np
import matplotlib as mpl
from iris.util import unify_time_units
from iris.util import equalise_attributes

def clean_callback(cube,field,filename):
    cube.coord('time').attributes = {}

# read prec file.
pr_file = '/Users/lais3/Desktop/prec_conc/MERRA2.tavg1_2d_flx_Nx.2019.SUB.nc'

pr = iris.load_cube(pr_file, 'total_precipitation', callback=clean_callback)


pr_file = '/Users/lais3/Desktop/prec_conc/MERRA2.tavg1_2d_flx_Nx.2020.SUB.nc'

pr_n = iris.load_cube(pr_file, 'total_precipitation', callback=clean_callback)

# pr_n.remove_coord('day_of_year')

cube = iris.cube.CubeList([pr,pr_n])
iris.util.unify_time_units(cube)
equalise_attributes(cube)
pr = cube.concatenate_cube()

'''
yy = np.arange(1981,2019,1,dtype=int)
yy = list(yy)

for i in yy:
    print(i)
    # read prec file.
    pr_file = '/Users/lais3/Desktop/prec_conc/MERRA2.tavg1_2d_flx_Nx.'+str(i)+'.SUB.nc'
    pr_n = iris.load_cube(pr_file, 'total_precipitation', callback=clean_callback)

    cube = iris.cube.CubeList([pr,pr_n])
    iris.util.unify_time_units(cube)
    equalise_attributes(cube)
    pr = cube.concatenate_cube()'''
    
iris.save(pr,'/Users/lais3/Desktop/prec_conc/MERRA2.tavg1_2d_flx_Nx.2019-2020.nc')

