#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 17:27:44 2020

@author: Lais
"""

""" 2. Loading Iris cubes - Examples from http://scitools.org.uk/iris/
docs/latest/userguide """


import iris

filename = iris.sample_data_path('uk_hires.pp')
cubes = iris.load(filename)
print(cubes)

# get the first cube (list indexing is 0 based)
air_potential_temperature = cubes[0]
print(air_potential_temperature)

# 2.1 Loading multiple files
# read more than one file into a list of cubes, listing the filenames
filenames = [iris.sample_data_path('uk_hires.pp'),
             iris.sample_data_path('air_temp.pp')]
cubes = iris.load(filenames)

# 2.2 Lazy loading
# 2.3 Constrained loading
# read files with star wildcards
filename = iris.sample_data_path('GloSea4', '*.pp')
cubes = iris.load(filename)

# constrain loading to surface_altitude only
filename = iris.sample_data_path('uk_hires.pp')
cubes = iris.load(filename, 'surface_altitude')

# constrain loading using STASH
filename = iris.sample_data_path('uk_hires.pp')
cubes = iris.load(filename, 'm01s00i033')

# constrain against both a standard name of surface_altitude and a STASH 
# of m01s00i033
filename = iris.sample_data_path('uk_hires.pp')
constraint = iris.NameConstraint(standard_name= 'surface_altitude', STASH='m01s00i033')
cubes = iris.load(filename, constraint)

# constrain the load to multiple distinct constraints
filename = iris.sample_data_path('uk_hires.pp')
cubes = iris.load(filename, ['air_potential_temperature','surface_altitude'])
                             
# constrain the load to match a specific model_level_number
filename = iris.sample_data_path('uk_hires.pp')
level_10 = iris.Constraint(model_level_number=10)
cubes = iris.load(filename, level_10)

# constrain the load using &
filename = iris.sample_data_path('uk_hires.pp')
forecast_6 = iris.Constraint(forecast_period=6)
level_10 = iris.Constraint(model_level_number=10)
cubes = iris.load(filename, forecast_6 & level_10)

# constrain the load using & in a list of values given to constrain a coordinate
filename = iris.sample_data_path('uk_hires.pp')
level_10_or_16_fp_6 = iris.Constraint(model_level_number=[10, 16], forecast_period=6)
cubes = iris.load(filename,level_10_or_16_fp_6)

# limit the value of a coordinate to a specific range, by passing the constraint
#as a function
def bottom_16_levels(cell):
    # return True or False as to whether the cell in question should be kept
    return cell <= 16

filename = iris.sample_data_path('uk_hires.pp')
level_lt_16 = iris.Constraint(model_level_number=bottom_16_levels)
cubes = iris.load(filename, level_lt_16)

# the simple function above can be written as a lambda function on a single line
bottom_16_levels = lambda cell: cell <= 16

# cube attributes can also be part of the constraint criteria
# from a cube attribute of STASH, the specific STASH codes can be filtered
filename = iris.sample_data_path('uk_hires.pp')
level_10_with_stash = iris.AttributeConstraint(STASH='m01s00i004') & iris.Constraint(model_level_number=10)
cubes = iris.load(filename, level_10_with_stash)

# 2.3.1 Constraining a circular coordinate across its boundary
# 2.3.2 Constraining on time
# iris will convert time-coordinate values (points and bounds) from numbers into
# datetime
filename = iris.sample_data_path('uk_hires.pp')
cube_all = iris.load_cube(filename, 'air_potential_temperature')
print('All times :\n' + str(cube_all.coord('time')))

# define a function which accepts a datetime as its argument
# (this is simplified in later examples)
hour_11 = iris.Constraint(time=lambda cell: cell.point.hour == 11)
cube_11 = cube_all.extract(hour_11)
print('Selected times :\n' + str(cube_11.coord('time')))

# an object can be compared to objects, and this comparison will then
# test only specific aspects from objects
import datetime
from iris.time import PartialDateTime
dt = datetime.datetime(2011, 3, 7)
print(dt > PartialDateTime(year=2010, month=6))

# the previous example can be written as
the_11th_hour = iris.Constraint(time=iris.time.PartialDateTime(hour=11))
print(iris.load_cube(
    iris.sample_data_path('uk_hires.pp'),
    'air_potential_temperature' & the_11th_hour).coord('time'))

# a cube constrained between two given dates
print(cube_all.coord('time'))

d1 = datetime.datetime.strptime('20091119T1100Z', '%Y%m%dT%H%MZ')
d2 = datetime.datetime.strptime('20091119T1200Z', '%Y%m%dT%H%MZ')
st_swithuns_daterange_07 = iris.Constraint(
    time=lambda cell: d1 <= cell.point < d2)
within_st_swithuns_07 = cube_all.extract(st_swithuns_daterange_07)
print(within_st_swithuns_07.coord('time'))

# rewrite using objects
pdt1 = PartialDateTime(year=2009, month=11, day=19)
pdt2 = PartialDateTime(year=2009, month=11, day=19)
st_swithuns_daterange_07 = iris.Constraint(
    time=lambda cell: pdt1 <= cell.point < pdt2)
print(within_st_swithuns_07.coord('time'))

ufile = '/home/oem/Desktop/for_lais_cp/be362.jan-dec_dmeans_ts.years1-30.u200850.nc'
uwnd = iris.load_cube(ufile)
print('All times :\n' + str(uwnd.coord('time')))

st_swithuns_daterange = iris.Constraint(
    time=lambda cell: PartialDateTime(month=11, day=19) <= cell
    < PartialDateTime(month=11, day=20))
within_st_swithuns_07 = cube_all.extract(st_swithuns_daterange)
print(within_st_swithuns_07.coord('time'))

# 2.4 Strict loading
# load a simple cube
filename = iris.sample_data_path('air_temp.pp')
cube = iris.load_cube(filename)
print(cube)

filename = iris.sample_data_path('uk_hires.pp')
cube = iris.load_cube(filename)

import iris
filename = iris.sample_data_path('uk_hires.pp')
air_pot_temp = iris.load_cube(filename, 'air_potential_temperature')
print(air_pot_temp)

# load 2 cubes
import iris
filename = iris.sample_data_path('uk_hires.pp')
altitude_cube, pot_temp_cube = iris.load_cubes(filename, ['surface_altitude',
                               'air_potential_temperature'])

# lists of a pre-known length and order can be exploited using multiple
# assignment
number_one, number_two = [1, 2]
print(number_one)
print(number_two)


















