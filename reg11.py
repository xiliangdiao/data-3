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
from sklearn import linear_model

data1 = np.loadtxt("/ihesp/fudan1991/pub/GlobalSST_0021_0501.txt")
SST = data1[130:480]

data=nc.Dataset('/ihesp/fred.castruccio/B1850/B.E.13.B1850C5.ne120_t12.sehires38.003.sunway_02.pop.h.AICE.002101.050112.nc')
res = np.zeros([2,20])

lon = np.arange(450,470,10)
lat = np.arange(3100,3300,10)

for idx,item in enumerate(lon):
    for jdx,jtem in enumerate(lat):
        plotvar = data.variables['aice'][:,item,jtem]
        if np.isnan(plotvar).sum()==0:
            A = np.arange(0,350)
            B = np.zeros(350)
            for ii in A:
                B[ii]=plotvar[ii*12 +9]
            regr = linear_model.LinearRegression()
            regr.fit(SST.reshape(-1, 1), B)
            a = regr.coef_
            res[idx,jdx]=a
        else:
            res[idx,jdx]=np.nan
    np.savetxt('new3100-13.out',res)