#!/usr/bin/env python3

""" Regridding the ERA-Interim data (200 hPa) for the u-be362 resolution"""

import numpy as np
import matplotlib.cm as mpl_cm
import matplotlib.pyplot as plt
import matplotlib.colors
import iris
import iris.analysis
import iris.plot as iplt
import iris.quickplot as qplt

# load two cubes that have different grids and coordinate systems.
# u_be362 STRF 200 hPa.
sf_file = '/media/oem/Elements/for_lais/be362.jan-dec_dmeans_ts.years1-30.sf200850.nc'
# Define the constraint at 200 hPa level
level_200 = iris.Constraint(air_pressure=200)
sf_n96 = iris.load_cube(sf_file, level_200)

# # Find Level = 200 hPa.
# levels = sf_n96.coord('air_pressure')
# print(levels.points)

start_year = 1979
stop_year = 2009
sf_file2 = '/media/oem/Elements/nc_files/ERA-INTERIM/STRF200/ERA.jan-dec_dmeans_ts.1979-2009.sf200.nc'

for year in range(start_year,stop_year+1):
    print(year)
    year_constraint = iris.Constraint(t=lambda cell: cell.point.year == year)
    sf_ERA = iris.load_cube(sf_file2, year_constraint)
    sf = sf_ERA.regrid(sf_n96, iris.analysis.Linear())
    # Save this year of streamfunction data to a file
    sf_file3 = '/media/oem/Elements/nc_files/ERA-INTERIM/STRF200_n96/STRF.'+str(year)+'.global_domain.nc'
    iris.save(sf,sf_file3)

























