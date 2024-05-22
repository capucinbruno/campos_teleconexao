#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 10:14:55 2020

@author: Laís
"""

""" 3. Saving Iris cubes - Examples from http://scitools.org.uk/iris/
docs/latest/userguide """

import iris

filename = iris.sample_data_path('uk_hires.pp')
cubes = iris.load(filename)
iris.save(cubes,'/tmp/uk_hires.nc')# where is tmp? see later

# do not do that (data is lost)
# cube = iris.load_cube('somefile.nc')
# iris.save(cube, 'somefile.nc')


# 3.1 Controlling the save process
# Save a cube to PP
iris.save(cubes[0], "myfile.pp")
# Save a cube list to a PP file, appending to the contents of the file
# if it already exists
iris.save(cubes,"myfile.pp", append=True)
# Save a cube to netCDF, defaults to NETCDF4 file format
iris.save(cubes[0],"myfile.nc")
# Save a cube list to netCDF, using the NETCDF3_CLASSIC storage option
iris.save(cubes, "myfile.nc", netcdf_format="NETCDF3_CLASSIC")

# 3.2 Customizing the save process
def tweaked_messages(cube):
    for cube, grib_message in iris.fileformats.grib.as_pairs(cube):
        # post process the GRIB2 message, prior to saving
        if cube.name() == 'carefully_customised_precipitation_amount':
            gribapi.grib_set_long(grib_message, "typeOfStatisticalProcess", 1)
            gribapi.grib_set_long(grib_message, "parameterCategory", 1)
            gribapi.grib_set_long(grib_message, "parameterNumber", 1)
        yield grib_message
iris.fileformats.grib.save_messages(tweaked_messages(cubes[0]), 'agrib2.grib2')
# Error iris.fileformats has no attribute grib

def tweaked_fields(cube):
    for cube, field in iris.fileformats.pp.save_pairs_from_cube(cube):
        # post process the PP field, prior to saving
        if cube.name() == 'air_pressure':
            field.lbexp = 'meaxp'
        elif cube.name() == 'air_density':
            field.lbexp = 'meaxr'
        yield field
iris.fileformats.pp.save_fields(tweaked_fields(cubes[0]), 'app.pp')

filename = '/home/oem/Desktop/python_scripts/Iris_examples/app.pp'
app = iris.load(filename)
# I could not understand!

























