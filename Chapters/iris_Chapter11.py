#!/usr/bin/env python3

""" 11. Basic cube mathematics
Examples from http://scitools.org.uk/iris/docs/latest/userguide """

import datetime
from datetime import timedelta

import iris
import iris.analysis
import iris.analysis.cartography
import iris.coords
import iris.coord_categorisation

# 11.1 Calculating the difference between two cubes
filename = iris.sample_data_path('E1_north_america.nc')
air_temp = iris.load_cube(filename,'air_temperature')

# get the first and last time slices
t_first = air_temp[0,:,:]
t_last = air_temp[-1,:,:]

# subtract the two
print(t_last - t_first)

# 11.2 Calculating a cube anomaly
print(air_temp.summary(True))

# calculate the time series mean using the collapsed method
air_temp_mean = air_temp.collapsed('time', iris.analysis.MEAN)
print(air_temp_mean.summary(True))

# calculate the time mean anomaly
anomaly = air_temp - air_temp_mean
print(anomaly.summary(True))

# first, create the transpose of the air temperature time-series
air_temp_T = air_temp.copy()
air_temp_T.transpose()
print(air_temp_T.summary(True))

# add the transpose to the original time-series
result = air_temp + air_temp_T
print(result.summary(True))

result == 2 * air_temp

# taking a slice from the middle latitude dimension
air_temp_T_slice = air_temp_T[:,0,:]
print(air_temp_T_slice.summary(True))

result = air_temp - air_temp_T_slice
print(result.summary(True))

# 11.3 Combining multiple phenomena to form a new one
filename = iris.sample_data_path('colpex.pp')
phenomenon_names = ['air_potential_temperature', 'air_pressure']
pot_temperature, pressure = iris.load_cubes(filename, phenomenon_names)

p0 = iris.coords.AuxCoord(1000.0,
                          long_name='reference_pressure',
                          units='hPa')
p0.convert_units(pressure.units)

temperature = pot_temperature*((pressure / p0)**(287.05/1005))
temperature.rename('air_temperature')




































