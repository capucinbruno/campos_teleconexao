#!/usr/bin/env python3

""" 8. Cube interpolation and regridding - 
Examples from http://scitools.org.uk/iris/docs/latest/userguide """

from __future__ import(absolute_import, division, print_function)
from six.moves import(filter, input, map, range, zip) # noqa

import iris
import iris.quickplot as qplt
import iris.analysis
import matplotlib.pyplot as plt
import numpy as np

# 8.1 Interpolation
air_temp = iris.load_cube(iris.sample_data_path('air_temp.pp'))
print(air_temp)

# We can interpolate specific values from the coordinates of the cube
sample_points = [('latitude', 51.48),('longitude', 0)]
print(air_temp.interpolate(sample_points, iris.analysis.Linear()))

result = air_temp.interpolate([('longitude', 0)], iris.analysis.Linear())
print('Original: ' + air_temp.summary(shorten=True))
print('Interpolated: ' + result.summary(shorten=True))

sample_points = [('longitude', np.linspace(-11, 2, 14)),
                 ('latitude', np.linspace(48, 60, 13))]
result = air_temp.interpolate(sample_points, iris.analysis.Linear())
print(result.summary(shorten=True))

lat_coord = air_temp.coord('latitude')
lat_points = lat_coord.points

lon_coord = air_temp.coord('longitude')
lon_points = lon_coord.points # lon doesn't have negative values, why??

# 8.1.1. Interpolating non-horizontal coordinates
fname = iris.sample_data_path('hybrid_height.nc')
column = iris.load_cube(fname, 'air_potential_temperature')[:, 0, 0]

alt_coord = column.coord('altitude')

# Interpolate the "perfect" linear interpolation. Really this is just
#a high number of interpolation points, in this case 1000 of them
altitude_points = [('altitude', np.linspace(400, 1250, 1000))]
scheme = iris.analysis.Linear(extrapolation_mode='mask')
linear_column = column.interpolate(altitude_points, scheme)
print(linear_column.coord('altitude').points)

# Now interpolate the data onto 10 evenly spaced altitude levels,
# as we did in the example
altitude_points = [('altitude', np.linspace(400, 1250, 10))]
scheme = iris.analysis.Linear()
new_column = column.interpolate(altitude_points, scheme)
print(new_column.coord('altitude').points)

plt.figure(figsize=(5,4), dpi=100)

# Plot the black markers for the original data
qplt.plot(column, column.coord('altitude'),
          marker='o', color='black', linestyle='', markersize=3,
          label='Original values', zorder=2)

# Plot the gray line to display the linear interpolation
qplt.plot(linear_column, linear_column.coord('altitude'),
          color='gray', 
          label='Linear Interpolation', zorder=0)

# Plot the red markers for the new data
qplt.plot(new_column, new_column.coord('altitude'),
          marker='D', color='red', linestyle='',
          label='Interpolated values', zorder=1)

ax = plt.gca()
# Space the plot such that the labels appear correctly
plt.subplots_adjust(left=0.17, bottom=0.14)

# Limit the plot to maximum of 5 ticks
ax.xaxis.get_major_locator().set_params(nbins=5)

# Prevent matplotlib from using "offset" notation on the xaxis
ax.xaxis.get_major_formatter().set_useOffset(False)

# Put some space between the line and the axes
ax.margins(0.05)

# Place gridlines and a legend
ax.grid()
plt.legend(loc='lower right')

plt.show()


# 8.1.2. Caching an interpolator ????
air_temp = iris.load_cube(iris.sample_data_path('air_temp.pp'))
interpolator = iris.analysis.Nearest().interpolator(air_temp,['latitude','longitude'])
latitudes = np.linspace(48, 60, 13)
longitudes = np.linspace(-11, 2, 14)
for lat, lon in zip(latitudes, longitudes):
    result = interpolator([lat, lon]) # ???
    

interpolator = iris.analysis.Nearest(extrapolation_mode='nan').interpolator(air_temp,['latitude','longitude'])


















