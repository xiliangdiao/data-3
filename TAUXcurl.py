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

data1=nc.Dataset('/ihesp/user/xiliangdiao/ihespdata/air500/TAUX/CESM_TAU_0291_.nc')
TAUX1 = data1.variables['TAUX'][0,80:160,-220:]
TAUX2 = data1.variables['TAUX'][0,80:160,:160]
TAUX = np.hstack((TAUX1,TAUX2))
lont1 = data1.variables['lon'][-220:]
lont2 = data1.variables['lon'][:160]
lont = np.hstack((lont1,lont2))
latt = data1.variables['lat'][80:160]

a = np.arange(0,80)
import math
#math.cos(math.radians(latt[:,3][399]))
wholedis = np.zeros(80)
for j in a:
    wholedis[j] = 111.34* math.cos(math.radians(latt[j]))
    
    

years = [f"{x:04d}" for x in range(0,1955)]
ii =0
result = np.zeros(1955)

for yy in years:
    data1=nc.Dataset('/ihesp/user/xiliangdiao/ihespdata/air500/TAUX/CESM_TAU_'+yy+'_.nc')
    TAUX1 = data1.variables['TAUX'][0,80:160,-220:]
    TAUX2 = data1.variables['TAUX'][0,80:160,:160]
    TAUX = np.hstack((TAUX1,TAUX2))
    lont1 = data1.variables['lon'][-220:]
    lont2 = data1.variables['lon'][:160]
    lont = np.hstack((lont1,lont2))
    latt = data1.variables['lat'][80:160]
    ###### (u2-u1)/(y2-y1)
    a = np.arange(0,79)
    A1= np.zeros([80,380])
    for i in a:
        A1[i,:] = (TAUX[i+1,:]-TAUX[i,:])/(0.25*110.95)
        ###################################
       
    data2=nc.Dataset('/ihesp/user/xiliangdiao/ihespdata/air500/TAUY/CESM_TAUY_'+yy+'_.nc')
    TAUY1 = data2.variables['TAUY'][0,80:160,-220:]
    TAUY2 = data2.variables['TAUY'][0,80:160,:160]
    TAUY = np.hstack((TAUY1,TAUY2))

        ####################################
        ###### (v2-v1)/(x2-x1)
    b = np.arange(0,379)
    A2= np.zeros([80,380])
    for j in a:
        for i in b:
            A2[j,i] = (TAUY[j,i+1]-TAUY[j,i])/(0.25*wholedis[j])
        #####################################
    A3 = A2[0:79,0:379] - A1[0:79,0:379]
        
    result[ii] = np.nanmean(A3)
        
    ii = ii + 1
#********************************************************************
    np.savetxt('new.out',result)
#np.savetxt('eastofmaudrise.out',result)