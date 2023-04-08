#!/usr/bin/env python3

""" Applying the Lanczos filter in the STRF anomalies (200 hPa) 
for the u-be362 simulation"""

import iris, iris.analysis
import iris.plot as iplt
import numpy as np
import matplotlib.pyplot as plt
from iris.time import PartialDateTime
from iris.util import unify_time_units
from iris.experimental.equalise_cubes import equalise_attributes
from iris.coord_categorisation import add_month

sf_file = '/home/oem/Desktop/python_scripts/tese/sf_a_be362.nc'
sf_a= iris.load_cube(sf_file)

# apply the Lanczos filter (20-90 days).
def low_pass_weights(window, cutoff):
    """Calculate weights for a low pass Lanczos filter.

    Args:

    window: int
        The length of the filter window.

    cutoff: float
        The cutoff frequency in inverse time steps.

    """
    order = ((window - 1) // 2) + 1
    nwts = 2 * order + 1
    w = np.zeros([nwts])
    n = nwts // 2
    w[n] = 2 * cutoff
    k = np.arange(1., n)
    sigma = np.sin(np.pi * k / n) * n / (np.pi * k)
    firstfactor = np.sin(2. * np.pi * cutoff * k) / (np.pi * k)
    w[n-1:0:-1] = firstfactor * sigma
    w[n+1:-1] = firstfactor * sigma
    return w[1:-1]

# 90 days band
# 1982
# copying values at the beginning and at the end for the periodic rolling window:
last105 = sf_a.extract(iris.Constraint(time = lambda cell: 
                                      PartialDateTime(year=1983, month=1, day=1) 
                                      <= cell.bound[0] <= 
                                      PartialDateTime(year=1983, month=4, day=15)))

first105 = sf_a.extract(iris.Constraint(time = lambda cell:
                                       PartialDateTime(year=2011, month=9, day=16) 
                                      <= cell.bound[0] <= 
                                      PartialDateTime(year=2011, month=12, day=30)))

sf_a_yr = sf_a.extract(iris.Constraint(time = lambda cell:
                                       PartialDateTime(year=1982, month=1, day=1) 
                                      <= cell.bound[0] <= 
                                      PartialDateTime(year=1982, month=12, day=30)))

periodic_time = iris.coords.DimCoord(np.arange(-105,465),standard_name='time',
                                     units='days since 1982-1-1 00:00:00')

lat_coord = sf_a.coord('latitude')
nlat = len(lat_coord.points)

lon_coord = sf_a.coord('longitude')
nlon = len(lon_coord.points) 

periodic_cube = iris.cube.Cube(data=np.zeros((570,nlat,nlon)),
                                dim_coords_and_dims=
                                [(periodic_time,0),(lat_coord,1),(lon_coord,2)])

periodic_cube.data[:105,:,:] = first105.data
periodic_cube.data[105:465,:,:] = sf_a_yr.data
periodic_cube.data[465:,:,:] = last105.data

# window length for filters.
window = 211

# construct 90 days low pass filter
# for the daily data.
wgts90 = low_pass_weights(window, 1. / 90.)
sf_a90 = sf_a_yr.copy()

for y in range(nlat):
    sf_a90.data[:,y,:] = periodic_cube[:,y,:].rolling_window(
        'time',iris.analysis.SUM,len(wgts90),weights=wgts90).data


# 1983 - 2010
start_year=1983
stop_year=2010

for year in range(start_year,stop_year+1):
    print(year)
    last105 = sf_a.extract(iris.Constraint(time = lambda cell: 
                                      PartialDateTime(year=year+1, month=1, day=1) 
                                      <= cell.bound[0] <= 
                                      PartialDateTime(year=year+1, month=4, day=15)))

    first105 = sf_a.extract(iris.Constraint(time = lambda cell:
                                       PartialDateTime(year=year-1, month=9, day=16) 
                                      <= cell.bound[0] <= 
                                      PartialDateTime(year=year-1, month=12, day=30)))

    sf_a_yr = sf_a.extract(iris.Constraint(time = lambda cell:
                                       PartialDateTime(year=year, month=1, day=1) 
                                      <= cell.bound[0] <= 
                                      PartialDateTime(year=year, month=12, day=30)))

    periodic_time = iris.coords.DimCoord(np.arange(-105,465),standard_name='time',
                                     units='days since '+str(year)+'-1-1 00:00:00')

   
    periodic_cube = iris.cube.Cube(data=np.zeros((570,nlat,nlon)),
                                dim_coords_and_dims=
                                [(periodic_time,0),(lat_coord,1),(lon_coord,2)])

    periodic_cube.data[:105,:,:] = first105.data
    periodic_cube.data[105:465,:,:] = sf_a_yr.data
    periodic_cube.data[465:,:,:] = last105.data

    sf_a90_yr = sf_a_yr.copy()

    for y in range(nlat):
        sf_a90_yr.data[:,y,:] = periodic_cube[:,y,:].rolling_window(
            'time',iris.analysis.SUM,len(wgts90),weights=wgts90).data
        
    cube = iris.cube.CubeList([sf_a90,sf_a90_yr])
    iris.util.unify_time_units(cube)
    equalise_attributes(cube)
    sf_a90 = cube.concatenate_cube()


# plot of the time series.
pdt1 = PartialDateTime(year=1982, month=1, day=1)
pdt2 = PartialDateTime(year=2011, month=1, day=1)
fst_29yrs = iris.Constraint(
    time=lambda cell: pdt1 <= cell.point < pdt2)
y_lat = iris.Constraint(latitude = -30)
x_lon = iris.Constraint(longitude = 355)
x = sf_a.extract(fst_29yrs & y_lat & x_lon )
x90 = sf_a90.extract(y_lat & x_lon )
  
# Plot the time series and the filtered version.
plt.figure(figsize=(9, 4))
iplt.plot(x, color='0.7', linewidth=1., linestyle='-',
          alpha=1., label='no filter')
iplt.plot(x90, color='r', linewidth=2., linestyle='-',
          alpha=.7, label='filter')
iplt.show()

# 2011
# copying values at the beginning and at the end for the periodic rolling window:
last105 = sf_a.extract(iris.Constraint(time = lambda cell: 
                                      PartialDateTime(year=1982, month=1, day=1) 
                                      <= cell.bound[0] <= 
                                      PartialDateTime(year=1982, month=4, day=15)))

first105 = sf_a.extract(iris.Constraint(time = lambda cell:
                                        PartialDateTime(year=2010, month=9, day=16) 
                                      <= cell.bound[0] <= 
                                      PartialDateTime(year=2010, month=12, day=30)))

sf_a_yr = sf_a.extract(iris.Constraint(time = lambda cell:
                                        PartialDateTime(year=2011, month=1, day=1) 
                                      <= cell.bound[0] <= 
                                      PartialDateTime(year=2011, month=12, day=30)))

periodic_time = iris.coords.DimCoord(np.arange(-105,465),standard_name='time',
                                      units='days since 2011-1-1 00:00:00')

periodic_cube = iris.cube.Cube(data=np.zeros((570,nlat,nlon)),
                                dim_coords_and_dims=
                                [(periodic_time,0),(lat_coord,1),(lon_coord,2)])

periodic_cube.data[:105,:,:] = first105.data
periodic_cube.data[105:465,:,:] = sf_a_yr.data
periodic_cube.data[465:,:,:] = last105.data

sf_a90_yr = sf_a_yr.copy()

for y in range(nlat):
    sf_a90_yr.data[:,y,:] = periodic_cube[:,y,:].rolling_window(
        'time',iris.analysis.SUM,len(wgts90),weights=wgts90).data

cube = iris.cube.CubeList([sf_a90,sf_a90_yr])
iris.util.unify_time_units(cube)
equalise_attributes(cube)
sf_a90 = cube.concatenate_cube()

iris.save(sf_a90, 'sf_a90_be362.nc')

'''
sf_file = '/home/oem/Desktop/python_scripts/tese/sf_a90_bd818.nc'
sf_a90= iris.load_cube(sf_file)
'''

# plot of the time series.
y_lat = iris.Constraint(latitude = -30)
x_lon = iris.Constraint(longitude = 355)
x = sf_a.extract(y_lat & x_lon )
x90 = sf_a90.extract(y_lat & x_lon )
  
# plot the time series and the filtered version.
plt.figure(figsize=(9, 4))
iplt.plot(x, color='0.7', linewidth=1., linestyle='-',
          alpha=1., label='no filter')
iplt.plot(x90, color='r', linewidth=2., linestyle='-',
          alpha=.7, label='filter')
iplt.show()

# change from low-pass to high-pass filter (90 days).
sf_a90_h = sf_a - sf_a90

# plot of the time series.
y_lat = iris.Constraint(latitude = -30)
x_lon = iris.Constraint(longitude = 355)
pdt1 = PartialDateTime(year=1982, month=1, day=1)
pdt2 = PartialDateTime(year=1983, month=1, day=1)
fst_yr = iris.Constraint(
    time=lambda cell: pdt1 <= cell.point < pdt2)
x = sf_a.extract(fst_yr & y_lat & x_lon )
x90 = sf_a90_h.extract(fst_yr & y_lat & x_lon )
  
# plot the time series and the filtered version.
plt.figure(figsize=(9, 4))
iplt.plot(x, color='0.7', linewidth=1., linestyle='-',
          alpha=1., label='no filter')
iplt.plot(x90, color='r', linewidth=2., linestyle='-',
          alpha=.7, label='filter')
iplt.show()

# plot of the time series.
y_lat = iris.Constraint(latitude = -30)
x_lon = iris.Constraint(longitude = 355)
pdt1 = PartialDateTime(year=1982, month=1, day=1)
pdt2 = PartialDateTime(year=1983, month=1, day=1)
fst_yr = iris.Constraint(
    time=lambda cell: pdt1 <= cell.point < pdt2)
x = sf_a.extract(fst_yr & y_lat & x_lon )
x90 = sf_a90.extract(fst_yr & y_lat & x_lon )
  
# plot the time series and the filtered version.
plt.figure(figsize=(9, 4))
iplt.plot(x, color='0.7', linewidth=1., linestyle='-',
          alpha=1., label='no filter')
iplt.plot(x90, color='r', linewidth=2., linestyle='-',
          alpha=.7, label='filter')
iplt.show()

# lon = sf_a.coord('longitude')
# lon = lon.points

# 20 days band
# fiter the remaining time-series with a 20-day low-pass filter.
# 1982
sf_a  = sf_a90_h.copy()

# copying values at the beginning and at the end for the periodic rolling window:
last105 = sf_a.extract(iris.Constraint(time = lambda cell: 
                                      PartialDateTime(year=1983, month=1, day=1) 
                                      <= cell.bound[0] <= 
                                      PartialDateTime(year=1983, month=4, day=15)))

first105 = sf_a.extract(iris.Constraint(time = lambda cell:
                                       PartialDateTime(year=2011, month=9, day=16) 
                                      <= cell.bound[0] <= 
                                      PartialDateTime(year=2011, month=12, day=30)))

sf_a_yr = sf_a.extract(iris.Constraint(time = lambda cell:
                                       PartialDateTime(year=1982, month=1, day=1) 
                                      <= cell.bound[0] <= 
                                      PartialDateTime(year=1982, month=12, day=30)))

periodic_time = iris.coords.DimCoord(np.arange(-105,465),standard_name='time',
                                     units='days since 1982-1-1 00:00:00')

lat_coord = sf_a.coord('latitude')
nlat = len(lat_coord.points)

lon_coord = sf_a.coord('longitude')
nlon = len(lon_coord.points) 

periodic_cube = iris.cube.Cube(data=np.zeros((570,nlat,nlon)),
                                dim_coords_and_dims=
                                [(periodic_time,0),(lat_coord,1),(lon_coord,2)])

periodic_cube.data[:105,:,:] = first105.data
periodic_cube.data[105:465,:,:] = sf_a_yr.data
periodic_cube.data[465:,:,:] = last105.data

# window length for filters.
window = 211

# construct 20 days low pass filter
# for the daily data.
wgts20 = low_pass_weights(window, 1. / 20.)

sf_a20 = sf_a_yr.copy()

for y in range(nlat):
    sf_a20.data[:,y,:] = periodic_cube[:,y,:].rolling_window(
        'time',iris.analysis.SUM,len(wgts20),weights=wgts20).data

# 1983 - 2010
start_year=1983
stop_year=2010

for year in range(start_year,stop_year+1):
    print(year)
    last105 = sf_a.extract(iris.Constraint(time = lambda cell: 
                                      PartialDateTime(year=year+1, month=1, day=1) 
                                      <= cell.bound[0] <= 
                                      PartialDateTime(year=year+1, month=4, day=15)))

    first105 = sf_a.extract(iris.Constraint(time = lambda cell:
                                       PartialDateTime(year=year-1, month=9, day=16) 
                                      <= cell.bound[0] <= 
                                      PartialDateTime(year=year-1, month=12, day=30)))

    sf_a_yr = sf_a.extract(iris.Constraint(time = lambda cell:
                                       PartialDateTime(year=year, month=1, day=1) 
                                      <= cell.bound[0] <= 
                                      PartialDateTime(year=year, month=12, day=30)))

    periodic_time = iris.coords.DimCoord(np.arange(-105,465),standard_name='time',
                                     units='days since '+str(year)+'-1-1 00:00:00')

   
    periodic_cube = iris.cube.Cube(data=np.zeros((570,nlat,nlon)),
                                dim_coords_and_dims=
                                [(periodic_time,0),(lat_coord,1),(lon_coord,2)])

    periodic_cube.data[:105,:,:] = first105.data
    periodic_cube.data[105:465,:,:] = sf_a_yr.data
    periodic_cube.data[465:,:,:] = last105.data

    sf_a20_yr = sf_a_yr.copy()

    for y in range(nlat):
        sf_a20_yr.data[:,y,:] = periodic_cube[:,y,:].rolling_window(
            'time',iris.analysis.SUM,len(wgts20),weights=wgts20).data
        
    cube = iris.cube.CubeList([sf_a20,sf_a20_yr])
    iris.util.unify_time_units(cube)
    equalise_attributes(cube)
    sf_a20 = cube.concatenate_cube()

iris.save(sf_a20, 'sf_a20_be362.nc')

'''
sf_file = '/home/oem/Desktop/python_scripts/tese/sf_a20_be362.nc'
sf_a20= iris.load_cube(sf_file, callback=clean_callback)
'''

# 2011
# copying values at the beginning and at the end for the periodic rolling window:
last105 = sf_a.extract(iris.Constraint(time = lambda cell: 
                                      PartialDateTime(year=1982, month=1, day=1) 
                                      <= cell.bound[0] <= 
                                      PartialDateTime(year=1982, month=4, day=15)))

first105 = sf_a.extract(iris.Constraint(time = lambda cell:
                                        PartialDateTime(year=2010, month=9, day=16) 
                                      <= cell.bound[0] <= 
                                      PartialDateTime(year=2010, month=12, day=30)))

sf_a_yr = sf_a.extract(iris.Constraint(time = lambda cell:
                                        PartialDateTime(year=2011, month=1, day=1) 
                                      <= cell.bound[0] <= 
                                      PartialDateTime(year=2011, month=12, day=30)))

periodic_time = iris.coords.DimCoord(np.arange(-105,465),standard_name='time',
                                      units='days since 2011-1-1 00:00:00')

periodic_cube = iris.cube.Cube(data=np.zeros((570,nlat,nlon)),
                                dim_coords_and_dims=
                                [(periodic_time,0),(lat_coord,1),(lon_coord,2)])

periodic_cube.data[:105,:,:] = first105.data
periodic_cube.data[105:465,:,:] = sf_a_yr.data
periodic_cube.data[465:,:,:] = last105.data

sf_a20_yr = sf_a_yr.copy()

for y in range(nlat):
    sf_a20_yr.data[:,y,:] = periodic_cube[:,y,:].rolling_window(
        'time',iris.analysis.SUM,len(wgts20),weights=wgts20).data

cube = iris.cube.CubeList([sf_a20,sf_a20_yr])
iris.util.unify_time_units(cube)
equalise_attributes(cube)
sf_a20 = cube.concatenate_cube()

# plot of the time series.
y_lat = iris.Constraint(latitude = -30)
x_lon = iris.Constraint(longitude = 355)
x = sf_a.extract(y_lat & x_lon )
x20 = sf_a20.extract(y_lat & x_lon )
  
# plot the time series and the filtered version.
plt.figure(figsize=(9, 4))
iplt.plot(x, color='0.7', linewidth=1., linestyle='-',
          alpha=1., label='no filter')
iplt.plot(x20, color='r', linewidth=2., linestyle='-',
          alpha=.7, label='filter')
iplt.show()


# select DJF days (order --> Jan / Feb / Dec).
# first Jan/Feb.
sf_a = sf_a20.copy()

pdt1 = PartialDateTime(year=1982, month=1, day=1)
pdt2 = PartialDateTime(year=1982, month=2, day=30)
Jan_Feb = iris.Constraint(
    time=lambda cell: pdt1 <= cell.bound[0] <= pdt2)

sf_a_Jan_Feb = sf_a.extract(Jan_Feb)

# last Dec.
pdt3 = PartialDateTime(year=2011, month=12, day=1)
pdt4 = PartialDateTime(year=2011, month=12, day=30)
Dec = iris.Constraint(
    time=lambda cell: pdt3 <= cell.bound[0] <= pdt4)

sf_a_Dec = sf_a.extract(Dec)

#1982/1983.
pdt5 = PartialDateTime(year=1982, month=12, day=1)
pdt6 = PartialDateTime(year=1983, month=2, day=30)
DJF = iris.Constraint(
    time=lambda cell: pdt5 <= cell.bound[0] <= pdt6)
sf_a_DJF = sf_a.extract(DJF)

#1983/84 to 2010/11.
start_year=1983
stop_year=2010

for year in range(start_year,stop_year+1):
    print(year)
    pdt7 = PartialDateTime(year=year, month=12, day=1)
    pdt8 = PartialDateTime(year=year+1, month=2, day=30)
    DJF_yrs = iris.Constraint(
    time=lambda cell: pdt7 <= cell.bound[0] <= pdt8)
    sf_a_DJF_yr = sf_a.extract(DJF_yrs)
    cube = iris.cube.CubeList([sf_a_DJF,sf_a_DJF_yr])
    iris.util.unify_time_units(cube)
    equalise_attributes(cube)
    sf_a_DJF = cube.concatenate_cube()


cube = iris.cube.CubeList([sf_a_Jan_Feb,sf_a_DJF,sf_a_Dec])
iris.util.unify_time_units(cube)
equalise_attributes(cube)
sf_a_DJF = cube.concatenate_cube()

iris.save(sf_a_DJF, 'STRFA_200hPa_DJF_be362.nc')













