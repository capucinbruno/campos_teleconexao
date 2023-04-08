#!/usr/bin/env python3

""" Example for rolling window function"""

import iris, iris.analysis
fname = iris.sample_data_path('GloSea4', 'ensemble_010.pp')
air_press = iris.load_cube(fname, 'surface_temperature')
print(air_press)

print(air_press.rolling_window('time', iris.analysis.MEAN, 3))
