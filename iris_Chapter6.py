#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 15:05:32 2020

@author: Lais
"""

""" 6. Real and Lazy Data - Examples from http://scitools.org.uk/iris/
docs/latest/userguide """

# 6.1 What is real and lazy data?
import iris
cube = iris.load_cube(iris.sample_data_path('air_temp.pp'))
cube.has_lazy_data()

cube.data # change the data for a real data (float, for instance)
cube.has_lazy_data()

# 6.3 When does my data become real?
# realise = converting lazy data into real data
cube = iris.load_cube(iris.sample_data_path('air_temp.pp'))
cube.has_lazy_data()

cube += 5 # I don't know what changes
cube.has_lazy_data()

# 6.3.1 Core data
cube = iris.load_cube(iris.sample_data_path('air_temp.pp'))
cube.has_lazy_data()

the_data = cube.core_data()
type(the_data)
cube.has_lazy_data()

# Realise the lazy data
cube.data
the_data = cube.core_data()
type(the_data)
cube.has_lazy_data()

# 6.4 Coordinates
cube = iris.load_cube(iris.sample_data_path('hybrid_height.nc'),'air_potential_temperature')

dim_coord = cube.coord('model_level_number')
print(dim_coord.has_lazy_points())
print(dim_coord.has_bounds())
print(dim_coord.has_lazy_points())

aux_coord = cube.coord('sigma')
print(aux_coord.has_lazy_points())
print(aux_coord.has_bounds())

# Realise the lazy points. This will **not** realise the lazy bounds
points = aux_coord.points
print(aux_coord.has_lazy_points())
print(aux_coord.has_lazy_bounds())

derived_coord = cube.coord('altitude')
print(derived_coord.has_lazy_points())
print(derived_coord.has_bounds())
print(derived_coord.has_lazy_bounds())














