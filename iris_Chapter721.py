#!/usr/bin/env python3

"""7.2.1. Plotting 1-dimensional cubes"""
from __future__ import(absolute_import, division, print_function)
from six.moves import(filter, input, map, range, zip) # noqa

import matplotlib.pyplot as plt

import iris
import iris.plot as iplt
import iris.quickplot as qplt

fname = iris.sample_data_path('air_temp.pp')
temperature = iris.load_cube(fname)

# Take a 1d slice using array style indexing
temperature_1d = temperature[5,:]

iplt.plot(temperature_1d)
plt.show()

# or
qplt.plot(temperature_1d)# quickplot
plt.show()

