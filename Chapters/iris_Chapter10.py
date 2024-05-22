#!/usr/bin/env python3

""" 10. Cube statistics
Examples from http://scitools.org.uk/iris/docs/latest/userguide """

# 10.1 Collapsing entire data dimensions
import datetime
from datetime import timedelta

import iris
import iris.analysis
import iris.analysis.cartography
import iris.coord_categorisation

filename = iris.sample_data_path('uk_hires.pp')
cube = iris.load_cube(filename, 'air_potential_temperature')
print(cube)

vertical_mean = cube.collapsed('model_level_number', iris.analysis.MEAN)
print(vertical_mean)

# 10.1.1. Area averaging
cube.coord('grid_latitude').guess_bounds()
cube.coord('grid_longitude').guess_bounds()
grid_areas = iris.analysis.cartography.area_weights(cube)

new_cube = cube.collapsed(['grid_longitude', 'grid_latitude'], iris.analysis.MEAN, weights=grid_areas)
print(new_cube)

# 10.2 Partially reducing data dimensions
# 10.2.1. Aggregation of grouped data
filename = iris.sample_data_path('ostia_monthly.nc')
cube = iris.load_cube(filename, 'surface_temperature')

iris.coord_categorisation.add_season(cube,'time', name='clim_season')
iris.coord_categorisation.add_season_year(cube,'time', name='season_year')
print(cube)

# These two coordinates can now be used to aggregate by season and climate-year
annual_seasonal_mean = cube.aggregated_by(
    ['clim_season','season_year'],
    iris.analysis.MEAN)
print(repr(annual_seasonal_mean))

# Printing the first 10 values of season+year from the original cube
for season, year in zip(cube.coord('clim_season')[:10].points,
                        cube.coord('season_year')[:10].points):
    print(season + '' + str(year))
    
clim_season = cube.coord('clim_season').points
season_year = cube.coord('season_year').points

# time = cube.coord('time').points
# time = cube.coord('time').units
# print(cube.coord('time'))
# print(cube.coord('time').units)

for season, year in zip(
        annual_seasonal_mean.coord('clim_season')[:10].points,
        annual_seasonal_mean.coord('season_year')[:10].points):
    print(season + '' + str(year))

print(annual_seasonal_mean.coord('time'))

# removing the resultant times which do not cover a three month period
tdelta_3mth = datetime.timedelta(hours=3*28*24.0)
spans_three_months = lambda t: (t.bound[1] - t.bound[0] > tdelta_3mth)
three_months_bound = iris.Constraint(time=spans_three_months)
full_season_means = annual_seasonal_mean.extract(three_months_bound)
full_season_means

# 17 seasons from jja-2006 to jja-2010
for season, year in zip(full_season_means.coord('clim_season').points,
                        full_season_means.coord('season_year').points):
    print(season + '' + str(year))
































