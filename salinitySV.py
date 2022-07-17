import netCDF4 as nc
import matplotlib.pyplot as plt
from matplotlib.colors import from_levels_and_colors
import numpy as np
from matplotlib import animation
from matplotlib.colors import BoundaryNorm
import matplotlib.colors as cols
import matplotlib as mpl
from mpl_toolkits.basemap import Basemap
from matplotlib import ticker, cm
import seaborn as sns

## the length
data1=nc.Dataset('/ihesp/user/xiliangdiao/ihespdata/ocn300/B.E.13.B1850C5.ne120_t12.sehires38.003.sunway_02.pop.h.0167-09.TAUX.nc')
lont = data1.variables['ULONG'][:600,1100:1600]
latt = data1.variables['ULAT'][:600,1100:1600]
latt[latt == -1.0] = np.nan
a = np.arange(0,600)
import math
wholedis = np.zeros(600)
for j in a:
    wholedis[j] = 111.34* math.cos(math.radians(latt[:,200][j]))
    
   
wholedis = wholedis * 1000 # 地球一度的距离(m)

# each layer depth (m)
data1=nc.Dataset('/ihesp/user/xiliangdiao/ihespdata/ocn300/B.E.13.B1850C5.ne120_t12.sehires38.003.sunway_02.pop.h.0330-12.dz.nc')
lev1 = data1.variables['dz'][:]/100
#########
months = [f"{x:02d}" for x in range(1,13)]
years = [f"{x:04d}" for x in range(270,310)]
ii=0
result = np.zeros(480)
for yy in years:
    for mm in months:
        data=nc.Dataset('/ihesp/user/xiliangdiao/ihespdata/ocn300/B.E.13.B1850C5.ne120_t12.sehires38.003.sunway_02.pop.h.'+yy+'-'+mm +'.VVEL.nc')
        plotvar = data.variables['VVEL'][0,:,:]
        v = plotvar[:,426,1100:1600]

##############################################
        plotvar[plotvar == -0.009999999776482582]= np.nan
        plotvar[plotvar == -1.0]= np.nan
        where_are_nan = np.isnan(plotvar)
        plotvar[where_are_nan] = 0
        v = v/100 # m/s

        data=nc.Dataset('/ihesp/user/xiliangdiao/ihespdata/ocn300/B.E.13.B1850C5.ne120_t12.sehires38.003.sunway_02.pop.h.'+yy+'-'+mm +'.SALT.nc')
        plotvar = data.variables['SALT'][0,:,:]
        salinity = plotvar[:,426,1100:1600]

##############################################
        salinity[salinity == -1000.0] = np.nan

###################################
#####  volume transport
        a = np.arange(0,500)
        A1= np.zeros([62,500])
        for j in a:
            A1[:,j] = v[:,j]* lev1[:]* 0.1 * wholedis[426] * salinity[:,j]
#####unit (m^3/s)
        A1[A1>100000000000000]=0
        final = np.nansum(A1,axis=1)
        streamSV = final/1000000
        streamSV[streamSV>=0]=np.nan
        result[ii] = np.nansum(streamSV)
        ii = ii + 1
        np.savetxt('/scratch/user/xiliangdiao/firstpaper/salt310-1.out',result)




