#!/usr/bin/env python3

""" 8.2 Regridding 
Examples from http://scitools.org.uk/iris/docs/latest/userguide """

import numpy as np
import matplotlib.cm as mpl_cm
import matplotlib.pyplot as plt
import matplotlib.colors
import iris
import iris.analysis
import iris.plot as iplt
import iris.quickplot as qplt

# load two cubes that have different grids and coordinate systems:
global_air_temp = iris.load_cube(iris.sample_data_path('air_temp.pp'))
rotated_psl = iris.load_cube(iris.sample_data_path('rotated_pole.nc'))

# regrid the global_air_temp cube onto a rotated pole grid using 
# a linear scheme
rotated_air_temp = global_air_temp.regrid(rotated_psl, iris.analysis.Linear())

# regrid the rotated_psl cube onto the global grid as defined by the 
# global_air_temp cube --> necessary defining the extrapolation mode
scheme = iris.analysis.Linear(extrapolation_mode='mask')
global_psl = rotated_psl.regrid(global_air_temp, scheme)

plt.figure(figsize=(4,3))
iplt.pcolormesh(global_psl)
plt.title('Air pressure\n'
          'on a global longitude latitude grid')
ax = plt.gca()
ax.coastlines()
ax.gridlines()
ax.set_extent([-90, 70, 10, 80])

plt.show()

# 8.2.1. Area-weighted regridding
global_air_temp = iris.load_cube(iris.sample_data_path('air_temp.pp'))
print(global_air_temp.summary(shorten=True))

regional_ash = iris.load_cube(iris.sample_data_path('NAME_output.txt'))
regional_ash = regional_ash.collapsed('flight_level', iris.analysis.SUM)
print(regional_ash.summary(shorten=True))

# mask any data that falls below a meaningful concentration
regional_ash.data = np.ma.masked_less(regional_ash.data, 5e-6)

norm = matplotlib.colors.LogNorm(5e-6, 0.0175)

global_air_temp.coord('longitude').guess_bounds()
global_air_temp.coord('latitude').guess_bounds()

fig = plt.figure(figsize=(8, 4.5))

plt.subplot(2, 2, 1)
iplt.pcolormesh(regional_ash, norm=norm)
plt.title('Volcanic ash total\nconcentration not regridded',
          size='medium')

for subplot_num, mdtol in zip([2, 3, 4],[0,0.5,1]):
    plt.subplot(2, 2, subplot_num)
    # regrid using the area weighted regridding scheme
    scheme = iris.analysis.AreaWeighted(mdtol=mdtol)
    global_ash = regional_ash.regrid(global_air_temp, scheme)
    iplt.pcolormesh(global_ash, norm=norm)
    plt.title('Volcanic ash total concentration\n'
              'regridded with AreaWeighted(mdtol={})'.format(mdtol),
          size='medium')
    
plt.subplots_adjust(hspace=0, wspace=0.05,
                    left=0.001, right=0.999, bottom=0, top=0.955)

# Iterate over each of the figure's axes, adding coastlines, gridlines
# and setting the extent
for ax in fig.axes:
    ax.coastlines('50m')
    ax.gridlines()
    ax.set_extent([-80, 40, 31, 75])

plt.show()

# or without iteration
# norm = matplotlib.colors.LogNorm(5e-6, 0.0175)
# scheme = iris.analysis.AreaWeighted(mdtol=0.5)
# global_ash = regional_ash.regrid(global_air_temp, scheme)
# print(global_ash.summary(shorten=True))

# 8.2.2. Caching a regridder
global_air_temp = iris.load_cube(iris.sample_data_path('air_temp.pp'))
rotated_psl = iris.load_cube(iris.sample_data_path('rotated_pole.nc'))
regridder = iris.analysis.Nearest().regridder(global_air_temp, rotated_psl)

# When this cached regridder is called you must pass it a cube on the same grid
# as the source grid cube (in this case, global_air_temp) that is to be
# regridded to the target grid
# for cube in list_of_cubes_on_source_grid:
#     result = regridder(cube)
#???










