#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 17:43:43 2020

@author: Lais
"""

""" 4. Navigating a cube - Examples from http://scitools.org.uk/iris/
docs/latest/userguide """

# 4.1 Cube string representations 
import iris
filename = iris.sample_data_path('rotated_pole.nc')
cube = iris.load_cube(filename)
print(cube)

print(str(cube))
print(repr(cube))
print(type(cube))

# 4.2 Working with cubes
print(cube.standard_name)
print(cube.long_name)
print(cube.units)

print(cube.name())

print(type(cube.data))

print(cube.shape)
print(cube.ndim)

# change the units of a cube 
cube.convert_units('hPa')

# acessing cell methods
print(cube.cell_methods)

# 4.3 Acessing coordinates on the cube
for coord in cube.coords():
    print(coord.name())

# use list comprehension to store the names
coord_names = [coord.name() for coord in cube.coords()]
print(', '.join(sorted(coord_names)))

# get an individual coordinate given its name
coord = cube.coord('grid_latitude')
print(type(coord))

print(coord.standard_name)
print(coord.long_name)
print(coord.units)

print(type(coord.points))
print(type(coord.bounds))

# Adding metadata to a cube
# add and remove coordinates
import iris.coords
new_coord = iris.coords.AuxCoord(1, long_name='my_custom_coordinate', units='no_unit')
cube.add_aux_coord(new_coord)
print(cube)

# 4.5 Adding and removing metadata to the cube at load time
filename = iris.sample_data_path('GloSea4', '*.pp')
print(iris.load(filename,'surface_temperature'))

filename = iris.sample_data_path('GloSea4', 'ensemble_001.pp')
realization = int(filename[-6:-3])
print(realization)

# add the apropriate metadata
import numpy as np
import iris 
import iris.coords as icoords

def lagged_ensemble_callback(cube, field, filename):
    # Add our own realization coordinate if it doesn't already exist
    if not cube.coords('realization'):
        realization = np.int32(filename[-6:-3])
        ensemble_coord = icoords.AuxCoord(realization, standard_name='realization')
        cube.add_aux_coord(ensemble_coord)
        
filename = iris.sample_data_path('GloSea4', '*.pp')

print(iris.load(filename, 'surface_temperature', callback=lagged_ensemble_callback))







































