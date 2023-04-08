#!/usr/bin/env python3

"""Compute Rossby wave source from the NCEP reanalysis wind data at 200 hPa, 
for 1979-2009
"""
import numpy as np
import cartopy.crs as ccrs
import iris, iris.analysis
import iris.plot as iplt
from iris.coord_categorisation import add_month
import matplotlib as mpl
import matplotlib.pyplot as plt
from iris.time import PartialDateTime

from windspharm.iris import VectorWind

mpl.rcParams['mathtext.default'] = 'regular'

yy = np.arange(1979,2010,1,dtype=int)
yy = list(yy)

for i in yy:
    print(i)
    # Read zonal and meridional wind components from file using the iris module.
    u_file = '/media/oem/Elements/nc_files/NCEP1/wind/uwnd/uwnd.'+str(i)+'.nc'
    v_file = '/media/oem/Elements/nc_files/NCEP1/wind/vwnd/vwnd.'+str(i)+'.nc'

    # Define the constraint at 200 hPa level
    level_200 = iris.Constraint(Level=200)

    uwnd = iris.load_cube(u_file,level_200)
    vwnd = iris.load_cube(v_file,level_200)

    uwnd.coord('longitude').circular = True
    vwnd.coord('longitude').circular = True

    # Create a VectorWind instance to handle the computations.
    w = VectorWind(uwnd, vwnd)

    # Compute components of rossby wave source: absolute vorticity, divergence,
    # irrotational (divergent) wind components, gradients of absolute vorticity.
    eta = w.absolutevorticity()
    div = w.divergence()
    uchi, vchi = w.irrotationalcomponent()
    etax, etay = w.gradient(eta)
    etax.units = 'm**-1 s**-1'
    etay.units = 'm**-1 s**-1'

    # Combine the components to form the Rossby wave source term.
    S = eta * -1. * div - (uchi * etax + vchi * etay)
    # S.coord('longitude').attributes['circular'] = True 
    # it does not work for saving (circular attribute)

    # Save this year of RWS data to a file
    S_file = '/media/oem/Elements/nc_files/NCEP1/RWS/RWS_200hPa_'+str(i)+'.nc'
    iris.save(S,S_file)

# Find Level = 200 hPa
# levels = uwnd.coord('Level')
# print(levels.points)

















