#!/usr/bin/env python3

""" Calculating STRF anomalies (200 hPa) for the u-be362 simulation"""

import cartopy.crs as ccrs
import iris, iris.analysis
import iris.plot as iplt
import numpy as np
import matplotlib.pyplot as plt
from iris.time import PartialDateTime
from iris.util import unify_time_units
from iris.experimental.equalise_cubes import equalise_attributes
from iris.coord_categorisation import add_day_of_year

# read STRF file.
sf_file = '/media/oem/Elements/for_lais/be362.jan-dec_dmeans_ts.years1-30.sf200850.nc'

# constraint between +/- 76 latitude.
lat_75 = iris.Constraint(latitude=lambda v: -76 <= v <= 76)

# constraint at 200 hPa level.
level_200 = iris.Constraint(air_pressure=200)
sf = iris.load_cube(sf_file, lat_75 & level_200)

# # verifying the new lat.
# lat = sf.coord('latitude')
# lat = lat.pointsthor: oem

# STRF plot for the first 10 of January
pdt = PartialDateTime(year=1982, month=1, day=10)
d10 = iris.Constraint(time=lambda cell: cell.bound[0] == pdt)
sf1 = sf.extract(d10)

# plot streamfunction.
plt.figure()
clevs = [-120, -100, -80, -60, -40, -20, 0, 20, 40, 60, 80, 100, 120]
ax = plt.subplot(111, projection=ccrs.PlateCarree(central_longitude=180))
fill_sf = iplt.contourf(sf1 * 1e-06, clevs, cmap=plt.cm.RdBu_r,
                        extend= 'both')
ax.coastlines()
ax.gridlines()
plt.colorbar(fill_sf, orientation= 'horizontal')
plt.title('Streamfunction ($10^6$m$^2$s$-1}$)',fontsize=16)
plt.show()

# STRF zonally assymetric.
sf_m = sf.collapsed('longitude', iris.analysis.MEAN)
sf_za = sf - sf_m

# STRF plot for the first 10 of January
sf1 = sf_za.extract(d10)

# plot the zonally assymetric streamfunction.
plt.figure()
clevs = [-120, -100, -80, -60, -40, -20, 0, 20, 40, 60, 80, 100, 120]
ax = plt.subplot(111, projection=ccrs.PlateCarree(central_longitude=180))
fill_sf = iplt.contourf(sf1 * 1e-05, clevs, cmap=plt.cm.RdBu_r,
                        extend= 'both')
ax.coastlines()
ax.gridlines()
plt.colorbar(fill_sf, orientation= 'horizontal')
plt.title('Zonally asymmetric streamfunction ($10^5$m$^2$s$-1}$)',fontsize=16)
plt.show()

# STRF's daily climatology. 
iris.coord_categorisation.add_day_of_year(sf_za, 'time', name='day_of_year')
sf_c = sf_za.aggregated_by(
    ['day_of_year'], iris.analysis.MEAN)

# STRF's climatology plot for the 10 of January.
pdt = PartialDateTime(month=1, day=10)
d10 = iris.Constraint(time=lambda cell: cell.bound[0] == pdt)
sf2 = sf_c.extract(d10)

# plot the climatological streamfunction.
plt.figure()
clevs = [-120, -100, -80, -60, -40, -20, 0, 20, 40, 60, 80, 100, 120]
ax = plt.subplot(111, projection=ccrs.PlateCarree(central_longitude=180))
fill_sf = iplt.contourf(sf2 * 1e-05, clevs, cmap=plt.cm.RdBu_r,
                        extend= 'both')
ax.coastlines()
ax.gridlines()
plt.colorbar(fill_sf, orientation= 'horizontal')
plt.title('Climatology streamfunction ($10^5$m$^2$s$-1}$)',fontsize=16)
plt.show()

# Copying values at the beginning and at the end for the periodic rolling window:
last15 = sf_c.extract(iris.Constraint(time = lambda cell: 
                                      PartialDateTime(month=12, day=16) 
                                      <= cell.bound[0] <= 
                                      PartialDateTime(month=12, day=30)))

first15 = sf_c.extract(iris.Constraint(time = lambda cell:
                                       PartialDateTime(month=1, day=1) 
                                      <= cell.bound[0] <= 
                                      PartialDateTime(month=1, day=15)))

periodic_time = iris.coords.DimCoord(np.arange(-15,375),standard_name='time',
                                     units='days since 1982-1-1 00:00:00')

lat_coord = sf_c.coord('latitude')
nlat = len(lat_coord.points)

lon_coord = sf_c.coord('longitude')
nlon = len(lon_coord.points) 

periodic_cube = iris.cube.Cube(data=np.zeros((390,nlat,nlon)),
                               dim_coords_and_dims=
                               [(periodic_time,0),(lat_coord,1),(lon_coord,2)])

periodic_cube.data[:15,:,:] = last15.data
periodic_cube.data[15:375,:,:] = sf_c.data
periodic_cube.data[375:,:,:] = first15.data

for y in range(nlat):
    sf_c.data[:,y,:] = periodic_cube[:,y,:].rolling_window('time',iris.analysis.MEAN,31).data
    
# STRF's climatology plot for the 10 of January.
pdt = PartialDateTime(month=1, day=10)
d10 = iris.Constraint(time=lambda cell: cell.bound[0] == pdt)
sf2 = sf_c.extract(d10)

# plot the climatological streamfunction (smoothed).
plt.figure()
clevs = [-120, -100, -80, -60, -40, -20, 0, 20, 40, 60, 80, 100, 120]
ax = plt.subplot(111, projection=ccrs.PlateCarree(central_longitude=180))
fill_sf = iplt.contourf(sf2 * 1e-05, clevs, cmap=plt.cm.RdBu_r,
                        extend= 'both')
ax.coastlines()
ax.gridlines()
plt.colorbar(fill_sf, orientation= 'horizontal')
plt.title('Climatology streamfunction smoothed ($10^5$m$^2$s$-1}$)',fontsize=14)
plt.show()

#STRF's anomaly.
first_year = 1982
year_constraint = iris.Constraint(time=lambda cell: cell.point.year == first_year)
sf_za_yr = sf_za.extract(year_constraint)
sf_a = sf_za_yr.copy()
sf_a.data = sf_za_yr.data - sf_c.data

start_year=1983
stop_year=2011

for year in range(start_year,stop_year+1):
    print(year)
    year_constraint = iris.Constraint(time=lambda cell: cell.point.year == year)
    sf_za_yr = sf_za.extract(year_constraint)
    sf_a_yr = sf_za_yr.copy()
    sf_a_yr.data = sf_za_yr.data - sf_c.data
    cube = iris.cube.CubeList([sf_a,sf_a_yr])
    iris.util.unify_time_units(cube)
    equalise_attributes(cube)
    sf_a = cube.concatenate_cube()

# STRF's anomaly plot for the first 10 of January
pdt = PartialDateTime(year=1982, month=1, day=10)
d10 = iris.Constraint(time=lambda cell: cell.bound[0] == pdt)
sf1 = sf_a.extract(d10)

# plot the anomaly streamfunction.
plt.figure()
clevs = [-120, -100, -80, -60, -40, -20, 0, 20, 40, 60, 80, 100, 120]
ax = plt.subplot(111, projection=ccrs.PlateCarree(central_longitude=180))
fill_sf = iplt.contourf(sf1 * 1e-05, clevs, cmap=plt.cm.RdBu_r,
                        extend= 'both')
ax.coastlines()
ax.gridlines()
plt.colorbar(fill_sf, orientation= 'horizontal')
plt.title('Anomaly streamfunction ($10^5$m$^2$s$-1}$)',fontsize=16)
plt.show()

iris.save(sf_a, 'sf_a_be362.nc')












