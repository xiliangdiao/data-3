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

# each layer depth (m)
data1=nc.Dataset('/ihesp/user/xiliangdiao/ihespdata/ocn300/B.E.13.B1850C5.ne120_t12.sehires38.003.sunway_02.pop.h.0330-12.dz.nc')
lev1 = data1.variables['dz'][:]/100
##########
data=nc.Dataset('/ihesp/user/xiliangdiao/ihespdata/ocn300/B.E.13.B1850C5.ne120_t12.sehires38.003.sunway_02.pop.h.0150-09.UVEL.nc')
lont = data.variables['ULONG'][:600,500:1100]
latt = data.variables['ULAT'][:600,500:1100]
#########
months = [f"{x:02d}" for x in range(1,2)]
years = [f"{x:04d}" for x in range(290,310)]
i =0
ii = 0
result = np.zeros(20)
####################################
for yy in years:
    for mm in months:
        data=nc.Dataset('/ihesp/user/xiliangdiao/ihespdata/ocn300/B.E.13.B1850C5.ne120_t12.sehires38.003.sunway_02.pop.h.'+yy+'-'+mm +'.UVEL.nc')
        plotvar = data.variables['UVEL'][0,:,:]
        plotvar[plotvar == -0.009999999776482582]= np.nan
        plotvar[plotvar == -1.0]= np.nan
        #where_are_nan = np.isnan(plotvar)
        #plotvar[where_are_nan] = 0
        #######################################################speed is here
        u = plotvar[:,0:600,500:1100]/100 #(m/s)
        a = np.arange(0,599)
        b = np.arange(0,600)
        A1= np.zeros([62,600,600])
        for j in a:
            for i in b:
                A1[:,j,i] = u[:,j,i] * lev1[:] * (latt[j+1,i]-latt[j,i])*110.95 * 1000  #(unit m)
        A1[A1>100000000000000]=0
        final = np.nansum(A1,axis=0)
        num = np.arange(1,599,1)
        stream = np.zeros([600,600])
        count = 0

        stream[0,:] = final[0,:]
        for i in num:
            stream[count+1,:] = stream[count,:]+final[i,:]
            count = count + 1
        result[ii] = stream.min()
        ii = ii + 1
        np.savetxt('/scratch/user/xiliangdiao/firstpaper/stream290-310-1.out',result)
        #np.savetxt(fname='/scratch/user/xiliangdiao/firstpaper/'+yy+'-'+mm +'data.csv', X=final,delimiter=",")
       