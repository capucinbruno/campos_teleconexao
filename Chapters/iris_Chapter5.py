#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  5 17:25:05 2020

@author: Lais
"""

""" 5. Subsetting a Cube - Examples from http://scitools.org.uk/iris/
docs/latest/userguide """

# 5.1 Cube extraction
import iris
filename = iris.sample_data_path('space_weather.nc')
cube = iris.load_cube(filename,'electron density')
equator_slice = cube.extract(iris.Constraint(grid_latitude=0))
print(equator_slice)

def near_zero(cell):
    """Returns true if the cell is between -0.1 and 0.1."""
    return -0.1 < cell < 0.1

equator_constraint = iris.Constraint(grid_latitude=near_zero)

# using the lambda function
equator_constraint = iris.Constraint(grid_latitude=lambda cell: -0.1 < cell < 0.1)

# selecting latitude between 15S and 15N
equator_slice2 = cube.extract(iris.Constraint(grid_latitude=lambda cell: -15.0 < cell < 15))

# get a height of 9000 m at the equator:
equator_height_9km_slice = equator_slice.extract(iris.Constraint(height=9000))
print(equator_height_9km_slice)

# simplifying the two previous steps into a single constraint:
equator_height_9km_slice = cube.extract(iris.Constraint(grid_latitude=0, height=9000))
print(equator_height_9km_slice)

# extract method on a CubeList
import iris
air_temp_and_fp_6 = iris.Constraint('air_potential_temperature', forecast_period=6)  
level_10 = iris.Constraint(model_level_number=10)
filename = iris.sample_data_path('uk_hires.pp')
cubes = iris.load(filename).extract(air_temp_and_fp_6 & level_10)
print(cubes)
print(cubes[0])

# 5.2 Cube iteration
# 3 dimensional cube (z,x,y) interating over all 2 dimensional slices in y and x
# which make up the full 3d cube
import iris
filename = iris.sample_data_path('hybrid_height.nc')
cubes = iris.load(filename)
cube = iris.load_cube(filename,'air_potential_temperature')
print(cube)
for i, yx_slice in enumerate(cube.slices(['grid_latitude','grid_longitude'])):
    print(i, repr(yx_slice))# 3D cube (15,100,100) 
    # 15 lat lon slices

import iris
filename = iris.sample_data_path('hybrid_height.nc')
cube = iris.load_cube(filename,'air_potential_temperature')
print(cube)
for i, x_slice in enumerate(cube.slices(['grid_longitude'])):
    print(i, repr(x_slice))# 3D cube (15,100,100) 
    # 15 lat lon slices
    
# get a single 2D slice 
first_slice = next(cube.slices(['grid_latitude', 'grid_longitude']))

# 5.3 Cube indexing
# examples of array indexing in numpy
import numpy as np
# create an array of 12 consecutive integers starting from 0
a = np.arange(12)
print(a)

print(a[0]) # first element of the array

print(a[-1]) # last element of the array

print(a[0:4]) # first four elements of the array (the same as a[:4])

print(a[-4:]) # last four elements of the array

print(a[::-1]) # gives all of the array, but backwards
    
# Make a 2d array by reshaping a
b = a.reshape(3,4)
print(b)

print(b[0, 0]) # first element of the first and second dimensions

print(b[0]) # first element of the first dimension (+ every other dimension)

# get the second element of the first dimension and all of the second dimension
# in reverse, by steps of two
print(b[1, ::-2])

# in iris, similarly
import iris
filename = iris.sample_data_path('hybrid_height.nc')
cube = iris.load_cube(filename,'air_potential_temperature')

print(cube)

# get the first element of the first dimension (+ every other dimension)
print(cube[0])

# get the last element of the first dimension (+ every other dimension)
print(cube[-1])

# get the first 4 elements of the first dimension (+ every other dimension)
print(cube[0:4])

# get the first element of the first and third dimension (+ every other dimension)
print(cube[0,:,0])

# get the second element of the first dimension and all of the second dimension
# in reverse, by steps of two
print(cube[1,::-2])





























































    