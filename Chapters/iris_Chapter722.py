#!/usr/bin/env python3

"""7.2.2. Plotting 2-dimensional cubes"""

# 7.2.2.1. Creating maps
# 7.2.2.2. Cube contour
from __future__ import(absolute_import, division, print_function)
from six.moves import(filter, input, map, range, zip) # noqa

import matplotlib.cm as mpl_cm
import matplotlib.pyplot as plt

import iris
import iris.quickplot as qplt

fname = iris.sample_data_path('air_temp.pp')
temperature_cube = iris.load_cube(fname)

# Add a contour, and put the result in a variable called contour
contour = qplt.contour(temperature_cube)

# Add coastlines to the map created by contour 
plt.gca().coastlines() # run joined the previous command

# Add contour labels based on the contour we have just created
plt.clabel(contour, inline=False) 

plt.show()

# 7.2.2.3. Cube filled contour
# Draw the contour with 25 levels
qplt.contourf(temperature_cube, 25)

# Add coastlines to the map created by contourf
plt.gca().coastlines()

plt.show()

# 7.2.2.4. Cube block plot
# Load the data for a single value of model level number
fname = iris.sample_data_path('hybrid_height.nc')
temperature_cube = iris.load_cube(
    fname, iris.Constraint(model_level_number=1))

# Draw the block plot
qplt.pcolormesh(temperature_cube)

plt.show()

# 7.3. Brewer colour palettes
# Plotting with Brewer
fname = iris.sample_data_path('air_temp.pp')
temperature_cube = iris.load_cube(fname)

# Load a Cynthia Brewer palette
brewer_cmap = mpl_cm.get_cmap('brewer_OrRd_09')

# Draw the contours, with n-levels set for the map colours (9)
# NOTE: needed as the map is non-interpolated, but matplotlib does not
# provide any special behaviour for these
qplt.contourf(temperature_cube, brewer_cmap.N, cmap=brewer_cmap)

# Add coastlines to the map created by contourf
plt.gca().coastlines()

plt.show()

# 7.3.3. Adding a citation
fname = iris.sample_data_path('air_temp.pp')
temperature_cube = iris.load_cube(fname)

# Get the Purples "Brewer" palette
brewer_cmap = plt.get_cmap('brewer_Purples_09')

# Draw the contours, with n-levels set for the map colours (9)
# NOTE: needed as the map is non-interpolated, but matplotlib does not
# provide any special behaviour for these
qplt.contourf(temperature_cube, brewer_cmap.N, cmap=brewer_cmap)

# Add a citation to the plot
iplt.citation(iris.plot.BREWER_CITE)

# Add coastlines to the map created by contourf
plt.gca().coastlines()

plt.show()
























